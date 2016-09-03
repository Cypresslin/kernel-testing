<?xml version='1.0' encoding='UTF-8'?>

<%
if 'root' in data:
    kt_root = data['root']
else:
    kt_root = '/var/lib/jenkins'

# deploy  = '$KT/cli-create %s $SUT %s' % (data['cloud'], data['series_name'])
deploy  = '$KT/cl create %s $SUT %s' % (data['cloud'], data['series_name'])
prepare = '$KT/cli-prepare %s $SUT --series %s' % (data['cloud'], data['series_name'])
tester  = '$KT/cli-test %s $SUT %s %s $KT_ROOT' % (data['cloud'], data['series_name'], data['test'])
%>

<project>
    <actions/>
    <description>
{}
    </description>
    <keepDependencies>false</keepDependencies>
    <properties>
    </properties>
    <scm class="hudson.scm.NullSCM"/>
    <assignedNode>master</assignedNode>
    <canRoam>false</canRoam>
    <disabled>false</disabled>
    <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    <triggers class="vector"/>
    <concurrentBuild>false</concurrentBuild>
    <builders>
        <hudson.tasks.Shell>
            <command>
export KT_ROOT=${kt_root}
KT=$KT_ROOT/kernel-testing

SSH_OPTIONS="${data['ssh_options']} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"

SUT=${data['sut_name']}

# Provision the hardware.
#
${deploy}
SUT_IP=`$KT/cl user-and-ip ${data['cloud']} $SUT`
${prepare}
${tester}

ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
scp $SSH_OPTIONS -r $SUT_IP:kernel-test-results $ARCHIVE
$JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results-unfiltered.xml
$KT/unicode-filter $WORKSPACE/kernel-results-unfiltered.xml > $WORKSPACE/kernel-results.xml

# Don't need the HW any longer, it can be powered off.
#
# $KT/cli-destroy ${data['cloud']} $SUT
$KT/cl destroy ${data['cloud']} $SUT

# Publish the results. This *MUST* always be the very last thing the job does.
#
if [ ! -e $ARCHIVE/no-tests ]; then
    $KT/test-results/mk-ingest-job --job-name=$JOB_NAME --build-id=$BUILD_ID --template=$KT/test-results/ingest-cloud-job.mako
fi
            </command>
        </hudson.tasks.Shell>

    </builders>
    <publishers>
        <hudson.tasks.junit.JUnitResultArchiver>
            <testResults>kernel-results.xml</testResults>
            <keepLongStdio>true</keepLongStdio>
            <testDataPublishers/>
        </hudson.tasks.junit.JUnitResultArchiver>
    </publishers>
    <buildWrappers>
      <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.29">
        <deleteDirs>false</deleteDirs>
        <cleanupParameter></cleanupParameter>
        <externalDelete></externalDelete>
      </hudson.plugins.ws__cleanup.PreBuildCleanup>
    </buildWrappers>
</project>
<!-- vi:set ts=4 sw=4 syntax=mako expandtab: -->

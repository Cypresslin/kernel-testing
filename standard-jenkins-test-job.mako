<?xml version='1.0' encoding='UTF-8'?>

<%
if 'root' in data:
    kt_root = data['root']
else:
    kt_root = '/var/lib/jenkins'
%>

<project>
    <actions/>
    <description>
${data['description']}
    </description>
    <keepDependencies>false</keepDependencies>
    <properties>
        <hudson.plugins.throttleconcurrents.ThrottleJobProperty>
            <maxConcurrentPerNode>1</maxConcurrentPerNode>
            <maxConcurrentTotal>100</maxConcurrentTotal>
            <categories>
                <string>${data['sut-name']}-hw-throttle</string>
            </categories>
            <throttleEnabled>true</throttleEnabled>
            <throttleOption>category</throttleOption>
        </hudson.plugins.throttleconcurrents.ThrottleJobProperty>
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

    status () {
        $KT/test-status $JOB_NAME '{"key":"'kernel.testing.job.status'", "op":"'$1'"}'
    }

    status job.started

    SSH_OPTIONS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"
    SUT=${data['sut-name']}

<%
provision = '$KT/metal --debug --nc'
provision += ' --series=%s --arch=%s' % (data['series-name'], data['sut-arch'])

if 'debs' in data:
    provision += ' --debs-url=%s' % data['debs']

if data['hwe']:
    provision += ' --hwe'

if data['ppa']:
    provision += ' --ppa=%s' % data['ppa']

if data['lkp']:
    provision += ' --lkp'

if data['kernel']:
    provision += ' --kernel=%s' % data['kernel']

if data['version']:
    provision += ' --required-kernel-version=%s' % data['version']

provision += ' $SUT'
%>
    # Provision the hardware.
    #
    ${provision} || (cat provisioning.log;status provisioning.failed;exit 1)
    status provisioning.succeeded

% if 'no-test' not in data:
    status testing.started
    # Kick off testing on the newly provisioned SUT
    #
    $KT/remote ubuntu@$SUT --kernel-test-list="${data['test']}"
    status testing.completed

    ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
    scp $SSH_OPTIONS -r ubuntu@$SUT:kernel-test-results $ARCHIVE
    $JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results-unfiltered.xml
    $KT/unicode-filter $WORKSPACE/kernel-results-unfiltered.xml > $WORKSPACE/kernel-results.xml

    # Don't need the HW any longer, it can be powered off.
    #
    $KT/release $SUT

    status job.completed

    # Publish the results. This *MUST* always be the very last thing the job does.
    #
    if [ ! -e $ARCHIVE/no-tests ]; then
        $KT/test-results/mk-ingest-job --job-name=$JOB_NAME --build-id=$BUILD_ID
    fi
% endif
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
    <buildWrappers/>
</project>
<!-- vi:set ts=4 sw=4 syntax=mako expandtab: -->

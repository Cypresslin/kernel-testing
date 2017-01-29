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
    if data['op'] == 'livepatch-snappy-client-payload-test':
        provision += ' --lkp-snappy'
    else:
        provision += ' --lkp'

if data['flavour']:
    provision += ' --flavour=%s' % data['flavour']

if data['kernel']:
    provision += ' --kernel=%s' % data['kernel']

if 'version' in data:
    if data['lkp']:
        provision += ' --required-kernel-version=%s' % data['kernel-version']
    else:
        provision += ' --required-kernel-version=%s' % data['version']

provision += ' $SUT'
%>
set +e
# Provision the hardware.
#
${provision}
if [ $? -ne 0 ]; then
    cat provisioning.log
    $KT/remote ubuntu@$SUT --kernel-test-list="${data['test']}"

    # Publish the results. This *MUST* always be the very last thing the job does.
    #
    if [ ! -e $ARCHIVE/no-tests ]; then
        $KT/test-results/mk-ingest-job --job-name=$JOB_NAME --build-id=$BUILD_ID
    fi
    exit -1
fi

% if 'no-test' not in data:
    # Kick off testing on the newly provisioned SUT
    #
    $KT/remote ubuntu@$SUT --kernel-test-list="${data['test']}"

    ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
    scp $SSH_OPTIONS -r ubuntu@$SUT:kernel-test-results $ARCHIVE
    $JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results-unfiltered.xml
    $KT/unicode-filter $WORKSPACE/kernel-results-unfiltered.xml > $WORKSPACE/kernel-results.xml

    # Don't need the HW any longer, it can be powered off.
    #
    $KT/release $SUT


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
    <buildWrappers>
      <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.29">
        <deleteDirs>false</deleteDirs>
        <cleanupParameter></cleanupParameter>
        <externalDelete></externalDelete>
      </hudson.plugins.ws__cleanup.PreBuildCleanup>
    </buildWrappers>
</project>
<!-- vi:set ts=4 sw=4 syntax=mako expandtab: -->

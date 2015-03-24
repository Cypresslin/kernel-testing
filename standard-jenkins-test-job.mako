<?xml version='1.0' encoding='UTF-8'?>
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
    KT=/var/lib/jenkins/kernel-testing

    $KT/test-status $JOB_NAME '{"op":"job.started"}'

    SSH_OPTIONS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"
    SUT=${data['sut-name']}

<%
provision = '$KT/provision $SUT'
provision += ' --sut=real --sut-series=%s --sut-arch=%s' % (data['series-name'], data['sut-arch'])

if 'debs' in data:
    provision += ' --sut-debs-url=%s' % data['debs']

if data['hwe']:
    provision += ' --sut-hwe'

if data['ppa']:
    provision += ' --ppa=%s' % data['ppa']

provision += ' --debug --nc'
%>
    # Provision the hardware.
    #
    ${provision} || (cat provisioning.log;$KT/test-status $JOB_NAME '{"op":"provisioning.failed"}';exit -1)
    $KT/test-status $JOB_NAME '{"op":"provisioning.succeeded"}'

% if 'no-test' not in data:
    $KT/test-status $JOB_NAME '{"op":"testing.started"}'
    # Kick off testing on the newly provisioned SUT
    #
    $KT/remote ubuntu@$SUT --kernel-test-list="${data['test']}"
    $KT/test-status $JOB_NAME '{"op":"testing.completed"}'

    ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
    scp $SSH_OPTIONS -r ubuntu@$SUT:kernel-test-results $ARCHIVE
    $JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results.xml

    # Don't need the HW any longer, it can be powered off.
    #
    $KT/release $SUT

    $KT/test-status $JOB_NAME '{"op":"job.completed"}'

    # Publish the results. This *MUST* always be the very last thing the job does.
    #
    $KT/test-results/mk-ingest-job --job-name=$JOB_NAME --build-id=$BUILD_ID
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

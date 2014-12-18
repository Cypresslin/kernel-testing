<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties>
        <hudson.plugins.throttleconcurrents.ThrottleJobProperty>
            <maxConcurrentPerNode>1</maxConcurrentPerNode>
            <maxConcurrentTotal>100</maxConcurrentTotal>
            <categories>
% if data.sut == 'virtual':
                <string>${data.vh_name}-hw-throttle</string>
% else:
                <string>${data.sut_name}-hw-throttle</string>
% endif
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
    SSH_OPTIONS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"

<%
if data.sut == 'virtual':
    provision = '$KT/provision %s' % (data.vh_name)
    provision += ' --sut=virtual --vh-series=%s --vh-arch=%s --sut-series=%s --sut-arch=%s' % (data.vh_series, data.vh_arch, data.sut_series, data.sut_arch)
    if data.vh_hwe:
        provision += ' --vh-hwe'
else:
    provision = '$KT/provision %s' % (data.sut_name)
    provision += ' --sut=real --sut-series=%s --sut-arch=%s' % (data.sut_series, data.sut_arch)

if data.debs is not None:
    provision += ' --sut-debs-url=%s' % data.debs

if data.sut_hwe:
    provision += ' --sut-hwe'

if data.ppa is not None:
    provision += ' --ppa=%s' % data.ppa
%>
    # Provision the hardware.
    #
    ${provision}

% if not data.no_test:
    # Kick off testing on the newly provisioned SUT
    #
    $KT/remote ${data.sut_name} --kernel-test-list="${data.test}"

    ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
    scp $SSH_OPTIONS -r ${data.sut_name}:kernel-test-results $ARCHIVE
    $JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results.xml

    # Publish the results
    #
    $KT/test-results/mk-ingest-job --job-name=$JOB_NAME --build-id=$BUILD_ID

    # Don't need the HW any longer, it can be powered off.
    #
    $KT/release ${data.sut_name}
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
<!-- vi:set ts=4 sw=4 expandtab: -->

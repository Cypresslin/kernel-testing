<--
{
    hwe : False,
    package : linux,
    url : https://bugs.launchpad.net/bugs/1410384,
    series-name : trusty,
    who : kernel,
    pocket : proposed,
    version : 3.13.0-45.74,
    key : kernel.publish.proposed.trusty,
    bug id : 1410384,
    date : 2015-01-26 20:09:48.928018,
    series-version : 10.04,
    op : sru,
    sut-arch : amd64,
    sut-name : rizzo,
}
-->

<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description>
        {
% for key in data:
            ${key} : ${data[key]},
% endfor
        }
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
    SSH_OPTIONS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"

<%
provision = '$KT/provision %s' % (data['sut-name'])
provision += ' --sut=real --sut-series=%s --sut-arch=%s' % (data['series-name'], data['sut-arch'])

if 'debs' in data:
    provision += ' --sut-debs-url=%s' % data['debs']

if data['hwe']:
    provision += ' --sut-hwe'

if 'ppa' in data:
    provision += ' --ppa=%s' % data['ppa']
%>
    # Provision the hardware.
    #
    ${provision}

% if 'no-test' not in data:
    # Kick off testing on the newly provisioned SUT
    #
    $KT/remote ubuntu@${data['sut-name']} --kernel-test-list="${data['test']}"

    ARCHIVE=$JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_ID/archive
    scp $SSH_OPTIONS -r ubuntu@${data['sut-name']}:kernel-test-results $ARCHIVE
    $JENKINS_HOME/autotest/client/tools/glue_testsuites $ARCHIVE/*.xml > $WORKSPACE/kernel-results.xml

    # Don't need the HW any longer, it can be powered off.
    #
    $KT/release ${data['sut-name']}

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

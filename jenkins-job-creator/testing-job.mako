<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
    <scm class="hudson.scm.NullSCM"/>
    <assignedNode>${data.sut_name}</assignedNode>
    <canRoam>false</canRoam>
    <disabled>false</disabled>
    <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    <triggers class="vector"/>
    <concurrentBuild>false</concurrentBuild>
    <builders>
        <hudson.tasks.Shell>
            <command># We utilize the jenkins slave, therefor this code is run on the test
# system and we need to pull any data from the jenkins server that is
# necessary for our testing.
#
set +e

# Clean up anything left over from previous runs.
#
sudo rm -rf *

# Fetch the relevant test scripts from the jenkins server
#
rsync -arv -e "ssh -o StrictHostKeyChecking=no" ${data.hw['jenkins server']}:autotest/ ./autotest/
rsync -arv -e "ssh -o StrictHostKeyChecking=no" ${data.hw['jenkins server']}:kernel-testing .

# This variable is unique to the jobs that the kernel team runs on their
# jenkins server.
#
export KERNEL_TEAM_JOB=&quot;true&quot;

export TESTS_CONTROL=" "
#export TESTS_CONTROL_UBUNTU=" "

# Make sure we have all the packages installed that we are going to
# need for these tests.
#
/bin/sh kernel-testing/pre-testing-setup

# Now run all the tests.
#
/bin/sh kernel-testing/kernel-tests-runner
            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers>
        <hudson.tasks.ArtifactArchiver>
            <artifacts>*.tbz2, *.json</artifacts>
            <latestOnly>false</latestOnly>
        </hudson.tasks.ArtifactArchiver>
        <hudson.tasks.junit.JUnitResultArchiver>
            <testResults>kernel-results.xml</testResults>
            <keepLongStdio>true</keepLongStdio>
            <testDataPublishers/>
        </hudson.tasks.junit.JUnitResultArchiver>
    </publishers>
    <buildWrappers/>
</project>

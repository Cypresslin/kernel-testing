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
                <string>${data.sut_name}-hw-throttle</string>
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
        <org.jvnet.hudson.plugins.SSHBuilder>
            <siteName>${data.hw['orchestra server']}</siteName>
            <command>
# Get rid of any previous profile (and system) with the same name
#
sudo cobbler profile remove --name=${data.sut_name}
sudo cobbler profile add --name=${data.sut_name} --distro=${data.sut_series}${data.sut_server_distro_decoration}-${data.sut_orchestra_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-${data.sut_preseed}-no-slave.preseed --repos=&quot;${data.sut_series}-${data.sut_orchestra_arch} ${data.sut_series}-${data.sut_orchestra_arch}-security&quot;
sudo cobbler system add --name=${data.sut_name} --profile=${data.sut_name} --hostname=${data.sut_name} --mac=${data.hw['mac address']}

# Power cycle the system so it will netboot and install
#
% for state in ['off', 'on']:
    % for psu in data.hw['cdu']:
        % if psu['ip'] != '':
            fence_cdu -a ${psu['ip']} -l ubuntu -p ubuntu -n ${psu['port']} -o ${state}
        % endif
    % endfor
% endfor

            </command>
        </org.jvnet.hudson.plugins.SSHBuilder>
        <hudson.tasks.Shell>
            <command>
export TARGET_HOST=${data.sut_name}

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $TARGET_HOST

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST

set +e # Continue if the node doesn&apos;t exist
./create-slave-node ${data.sut_name} $TARGET_HOST &quot;${data.sut_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:

# Enable the proposed pocket.
#
ssh -o StrictHostKeyChecking=no ${data.sut_name} 'echo deb http://us.archive.ubuntu.com/ubuntu/ ${data.sut_series}-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list'
ssh -o StrictHostKeyChecking=no ${data.sut_name} sudo apt-get update
ssh -o StrictHostKeyChecking=no ${data.sut_name} sudo apt-get --yes dist-upgrade

# If we are testing the lts-hwe package, get it installed and then reboot.
#
% if data.sut_hwe:
% if data.sut_hwe_series == 'quantal':
    scp -o StrictHostKeyChecking=no /var/lib/jenkins/kernel-testing/jenkins-job-creator/lts-hwe-development-install ${data.sut_name}:
    ssh -o StrictHostKeyChecking=no ${data.sut_name} /bin/sh lts-hwe-development-install
% else:
    ssh -o StrictHostKeyChecking=no ${data.sut_name} sudo apt-get update
    ssh -o StrictHostKeyChecking=no ${data.sut_name} sudo apt-get install --yes ${data.sut_hwe_package}
%endif
% endif

ssh -o StrictHostKeyChecking=no ${data.sut_name} sudo reboot
/var/lib/jenkins/kernel-testing/wait-for-system ${data.sut_name}
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh ${data.sut_name}:

# Copy the test script to the SUT and run it.
#
rm -f jenkins-env.sh; touch jenkins-env.sh
echo export BUILD_TAG=$BUILD_TAG >> jenkins-env.sh
echo export BUILD_ID=$BUILD_ID >> jenkins-env.sh
echo export JENKINS_HOME=$JENKINS_HOME >> jenkins-env.sh
echo export WORKSPACE=$WORKSPACE >> jenkins-env.sh
echo export JOB_NAME=$JOB_NAME >> jenkins-env.sh
set # See what environment variables are set
scp -o StrictHostKeyChecking=no /var/lib/jenkins/kernel-testing-bjf/jenkins-job-creator/kernel-tester ${data.sut_name}:
scp -o StrictHostKeyChecking=no jenkins-env.sh ${data.sut_name}:
ssh -o StrictHostKeyChecking=no ${data.sut_name} /bin/bash kernel-tester --kernel-test-list=${data.test} --kernel-test-options="${data.test_options}" --test-repository-host=${data.hw['jenkins server']}

% if not data.no_test:
set +e # No matter what, try to collect the results

# Publish the results
#
#/var/lib/jenkins/kernel-testing/test-results/ingest $HOME/jobs/$JOB_NAME/builds/$BUILD_ID
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

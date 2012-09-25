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
                <string>${data.vh_name}-hw-throttle</string>
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
sudo cobbler profile remove --name=${data.vh_name}
sudo cobbler profile add --name=${data.vh_name} --distro=${data.vh_series}${data.vh_server_distro_decoration}-${data.vh_orchestra_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-${data.vh_preseed}.preseed --repos=&quot;${data.vh_series}-${data.vh_orchestra_arch} ${data.vh_series}-${data.vh_orchestra_arch}-security&quot;
sudo cobbler system add --name=${data.vh_name} --profile=${data.vh_name} --hostname=${data.vh_name} --mac=${data.hw['mac address']}

sudo cobbler profile remove --name=${data.sut_name}
sudo cobbler profile add --name=${data.sut_name} --distro=${data.sut_series}${data.sut_server_distro_decoration}-${data.sut_orchestra_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-virt-${data.sut_preseed}.preseed --ksmeta=hostname=${data.sut_name} --virt-file-size=20,100 --virt-ram=1000 --virt-disk=raw,raw --virt-path=/opt/${data.sut_name}-a,/opt/${data.sut_name}-b

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

##################################################################
#
# V I R T U A L   H O S T
#
##################################################################
export TARGET_HOST=${data.vh_name}

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST

# Enable the proposed pocket on the vm host.
#
ssh -o StrictHostKeyChecking=no ${data.vh_name} 'echo deb http://us.archive.ubuntu.com/ubuntu/ ${data.vh_series}-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list'
ssh -o StrictHostKeyChecking=no ${data.vh_name} sudo apt-get update
ssh -o StrictHostKeyChecking=no ${data.vh_name} sudo apt-get --yes dist-upgrade

ssh -o StrictHostKeyChecking=no ${data.vh_name} sudo reboot
/var/lib/jenkins/kernel-testing/wait-for-system ${data.vh_name}

% if data.vh_series in ['lucid']:

# On Lucid series installs we have to install the jdk ourselves. There is
# no jenkins-slave package.
#
scp -o StrictHostKeyChecking=no /var/lib/jenkins/kernel-testing/jenkins-job-creator/manual-slave-install ${data.vh_name}:
ssh -o StrictHostKeyChecking=no ${data.vh_name} /bin/sh manual-slave-install

% endif

set +e # Continue if the node doesn&apos;t exist
./create-slave-node ${data.vh_name} $TARGET_HOST &quot;${data.vh_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:

##################################################################
#
# V I R T U A L   C L I E N T
#
##################################################################

# Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s ${data.jenkins_url} build -s ${data.vm_client_provisioning_job_name}

# Enable the proposed pocket on the SUT (the vm).
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

% if data.sut_series in ['lucid']:

# On Lucid series installs we have to install the jdk ourselves. There is
# no jenkins-slave package.
#
scp -o StrictHostKeyChecking=no /var/lib/jenkins/kernel-testing/jenkins-job-creator/manual-slave-install ${data.sut_name}:
ssh -o StrictHostKeyChecking=no ${data.sut_name} /bin/sh manual-slave-install

% endif

% if not data.no_test:
set +e # No matter what, try to collect the results

# Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s ${data.jenkins_url} build -s ${data.testing_job_name}

# Process the results
#
/var/lib/jenkins/kernel-testing/test-results/ingest $HOME/jobs/${data.testing_job_name}/builds/1
% endif
            </command>
        </hudson.tasks.Shell>

    </builders>
    <publishers/>
    <buildWrappers/>
</project>

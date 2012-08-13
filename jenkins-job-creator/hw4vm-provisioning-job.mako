<?xml version='1.0' encoding='UTF-8'?>
<%
if data.vh_series in ['lucid', 'natty']:
    vh_distro = ''
    vh_seed = 'secondary'
else:
    vh_distro = '-server'
    vh_seed = 'primary'

if data.sut_series in ['lucid', 'natty']:
    sut_distro = ''
    sut_seed = 'secondary'
else:
    sut_distro = '-server'
    sut_seed = 'primary'

if data.vh_arch == 'amd64':
    orchestra_vh_arch = 'x86_64'
else:
    orchestra_vh_arch = data.vh_arch

if data.sut_arch == 'amd64':
    orchestra_sut_arch = 'x86_64'
else:
    orchestra_sut_arch = data.sut_arch
%>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties>
        <hudson.plugins.throttleconcurrents.ThrottleJobProperty>
            <maxConcurrentPerNode>1</maxConcurrentPerNode>
            <maxConcurrentTotal>100</maxConcurrentTotal>
            <categories>
                <string>rizzo-hw-throttle</string>
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
sudo cobbler profile add --name=${data.vh_name} --distro=${data.vh_series}${vh_distro}-${orchestra_vh_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-${vh_seed}.preseed --repos=&quot;${data.vh_series}-${orchestra_vh_arch} ${data.vh_series}-${orchestra_vh_arch}-security&quot;
sudo cobbler system add --name=${data.vh_name} --profile=${data.vh_name} --hostname=${data.vh_name} --mac=${data.hw['mac address']}

sudo cobbler profile remove --name=${data.sut_name}
sudo cobbler profile add --name=${data.sut_name} --distro=${data.sut_series}${sut_distro}-${orchestra_sut_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-virt-${sut_seed}.preseed --ksmeta=hostname=${data.sut_name} --virt-file-size=20 --virt-ram=1000

% if data.hw['cdu']['ip'] != '':
# Power cycle the system so it will netboot and install
#
fence_cdu -a ${data.hw['cdu']['ip']} -l ubuntu -p ubuntu -n ${data.hw['cdu']['port']} -o off
fence_cdu -a ${data.hw['cdu']['ip']} -l ubuntu -p ubuntu -n ${data.hw['cdu']['port']} -o on
% endif
            </command>
        </org.jvnet.hudson.plugins.SSHBuilder>
        <hudson.tasks.Shell>
            <command>
export TARGET_HOST=${data.vh_name}

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $TARGET_HOST

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST

set +e # Continue if the node doesn&apos;t exist
./create-slave-node ${data.vh_name} $TARGET_HOST &quot;${data.vh_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:
            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
# Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s ${data.jenkins_url} build -s ${data.vm_client_provisioning_job_name}
            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
# Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s ${data.jenkins_url} build -s ${data.testing_job_name}
            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
# Publish the results
#
/var/lib/jenkins/kernel-testing/test-results/ingest $HOME/jobs/${data.testing_job_name}/builds/1
            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>

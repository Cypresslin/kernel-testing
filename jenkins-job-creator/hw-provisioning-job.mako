<?xml version='1.0' encoding='UTF-8'?>
<%
if data.sut_series in ['lucid', 'natty']:
    sut_distro = ''
    sut_seed = 'secondary'
else:
    sut_distro = '-server'
    sut_seed = 'primary'

if data.sut_arch == 'amd64':
    orchestra_arch = 'x86_64'
else:
    orchestra_arch = data.sut_arch
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
sudo cobbler profile remove --name=${data.sut_name}
sudo cobbler profile add --name=${data.sut_name} --distro=${data.sut_series}${sut_distro}-${orchestra_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-${sut_seed}.preseed --repos=&quot;${data.sut_series}-${orchestra_arch} ${data.sut_series}-${orchestra_arch}-security&quot;
sudo cobbler system add --name=${data.sut_name} --profile=${data.sut_name} --hostname=${data.sut_name} --mac=${data.hw['mac address']}

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
export TARGET_HOST=${data.sut_name}

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $TARGET_HOST

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST

set +e # Continue if the node doesn&apos;t exist
./create-slave-node ${data.sut_name} $TARGET_HOST &quot;${data.sut_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:
            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
# Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s ${data.jenkins_url} build -s ${data.testing_job_name}
            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>
<!-- vi:set ts=4 sw=4 expandtab: -->

<?xml version='1.0' encoding='UTF-8'?>
<%
if data.kernel_arch == 'amd64':
    orchestra_arch = 'x86_64'
else:
    orchestra_arch = data.kernel_arch
%>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
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
            <siteName>magners-orchestra</siteName>
            <command># Get rid of any previous profile (and system) with the same name
#
sudo cobbler profile remove --name=${data.test_host}
sudo cobbler profile add --name=${data.test_host} --distro=${data.target_series}-server-${orchestra_arch} --kickstart=/var/lib/cobbler/kickstarts/kernel/kt-primary.preseed --repos=&quot;${data.target_series}-${orchestra_arch} ${data.target_series}-${orchestra_arch}-security ${data.target_series}-${orchestra_arch}-updates&quot;
sudo cobbler system add --name=${data.test_host} --profile=${data.test_host} --hostname=${data.test_host} --mac=d4:ae:52:a3:6a:22

# Power cycle the system so it will netboot and install
#
fence_cdu -a 10.97.0.11 -l ubuntu -p ubuntu -n Rizzo_PS1 -o off
fence_cdu -a 10.97.0.11 -l ubuntu -p ubuntu -n Rizzo_PS1 -o on</command>
        </org.jvnet.hudson.plugins.SSHBuilder>
        <hudson.tasks.Shell>
            <command>set +e # Continue if the node doesn&apos;t exist

export TARGET_HOST=10.97.2.3

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $TARGET_HOST

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST
./create-slave-node ${data.test_host} $TARGET_HOST &quot;${data.kernel_arch} ${data.target_series}&quot;


# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -r /var/lib/jenkins/.ssh $TARGET_HOST:</command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command># Build the follow on job(s) waiting for them to finish.
#
java -jar /run/jenkins/war/WEB-INF/jenkins-cli.jar -s http://kernel-jenkins:8080 build -s ${data.test_host}-${data.target_series}-${data.kernel_arch}-test</command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers>
        <hudson.plugins.locksandlatches.LockWrapper>
            <locks>
                <hudson.plugins.locksandlatches.LockWrapper_-LockWaitConfig>
                    <name>rizzo</name>
                </hudson.plugins.locksandlatches.LockWrapper_-LockWaitConfig>
            </locks>
        </hudson.plugins.locksandlatches.LockWrapper>
    </buildWrappers>
</project>
<!-- vi:set ts=4 sw=4 expandtab: -->

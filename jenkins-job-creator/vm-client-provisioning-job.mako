<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
    <scm class="hudson.scm.NullSCM"/>
    <assignedNode>${data.vh_name}</assignedNode>
    <canRoam>false</canRoam>
    <disabled>false</disabled>
    <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    <triggers class="vector"/>
    <concurrentBuild>false</concurrentBuild>
    <builders>
        <hudson.tasks.Shell>
            <command>
cd /var/lib/jenkins
rm -rf kernel-testing
scp -o StrictHostKeyChecking=no -r ${data.hw['jenkins server']}:kernel-testing .

sudo apt-get install -y qemu-kvm koan virt-manager
sudo sed -ie 's/^\(libvirtd.*\)/\1jenkins/' /etc/group

# The file structure on an Ubuntu CD uses the string amd64 instead of x86_64. To
# use koan to install x86_64 VMs it is necessary (at least with cobbler on Oneiric)
# to modify one file.
#
sudo sed -i -e '/elif uri.count("installer-amd64"):/ i \ \ \ \ \ \ \ \ elif uri.count("x86_64"):\n\ \ \ \ \ \ \ \ \ \ \ \ self._treeArch = "amd64"' /usr/share/pyshared/virtinst/OSDistro.py

echo &quot;\n\nauto br0\niface br0 inet dhcp\n        bridge_ports     eth0\n        bridge_stp         off\n        bridge_fd            0\n        bridge_maxwait 0\n&quot; | sudo tee -a /etc/network/interfaces
sudo ifup br0

sudo koan --virt --server=${data.hw['orchestra server']} --profile=${data.sut_name} --virt-name=${data.sut_name} --virt-bridge=br0 --vm-poll

set +e

export TARGET_HOST=${data.sut_name}

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $TARGET_HOST

cd /var/lib/jenkins/kernel-testing
./wait-for-system $TARGET_HOST
./create-slave-node $TARGET_HOST $TARGET_HOST &quot;${data.sut_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:

            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>

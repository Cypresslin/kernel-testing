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
scp -r ${data.hw['jenkins server']}:kernel-testing .

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

ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R ${data.sut_name}

cd /var/lib/jenkins/kernel-testing
./wait-for-system ${data.sut_name}
./create-slave-node ${data.sut_name} ${data.sut_name} &quot;${data.sut_name}&quot;

# Fix .ssh config on slave so it can copy from kernel-jenkins
#
scp -r /var/lib/jenkins/.ssh ${data.sut_name}:

            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>

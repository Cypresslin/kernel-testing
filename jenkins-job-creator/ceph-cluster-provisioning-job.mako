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
# On the virtual-host we clean up any old cruft. However, in the usual case the virtual-host
# was reprovisioned from scratch so there shouldn't be anything to cleanup.
#
cd /var/lib/jenkins
rm -rf kernel-testing
rsync -ar --exclude '.git' -e "ssh -o StrictHostKeyChecking=no" ${data.hw['jenkins server']}:kernel-testing/ ./kernel-testing/
            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
# Instll the packages we require for creating VMs
#
sudo apt-get install -y qemu-kvm koan virt-manager

# We add the jenkins user to the libvirtd group so that we can run virt-manager
# if we need to. This is handy for debugging installation issues.
#
sudo sed -ie 's/^\(libvirtd.*\)/\1jenkins/' /etc/group

# Setup the bridged network for the VMs. This allows us to get to them from anywhere
# on the network.
#
echo &quot;\n\nauto br0\niface br0 inet dhcp\n        bridge_ports     eth0\n        bridge_stp         off\n        bridge_fd            0\n        bridge_maxwait 0\n&quot; | sudo tee -a /etc/network/interfaces
sudo ifup br0

            </command>
        </hudson.tasks.Shell>
        <hudson.tasks.Shell>
            <command>
for NODE in ceph-a ceph-b ceph-c; do
    # Provision a new VM
    #
    sudo koan --virt --server=${data.hw['orchestra server']} --profile=${data.sut_name} --virt-name=$NODE --virt-bridge=br0 --vm-poll

    # Wait for the new VM to come up and configure it's ssh so that we can do anything
    # we want with it.
    #
    set +e

    ssh-keygen -f &quot;/var/lib/jenkins/.ssh/known_hosts&quot; -R $NODE

    cd /var/lib/jenkins/kernel-testing
    ./wait-for-system $NODE
    ./create-slave-node $NODE $NODE &quot;$NODE&quot;

    # Fix .ssh config on slave so it can copy from kernel-jenkins
    #
    scp -o StrictHostKeyChecking=no -r /var/lib/jenkins/.ssh $TARGET_HOST:
done
            </command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>

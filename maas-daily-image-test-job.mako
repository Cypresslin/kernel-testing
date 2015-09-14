<?xml version='1.0' encoding='UTF-8'?>

<%
if 'root' in data:
    kt_root = data['root']
else:
    kt_root = '/var/lib/jenkins'
%>

<project>
    <actions/>
    <description>
${data['description']}
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
    export KT_ROOT=${kt_root}
    KT=$KT_ROOT/kernel-testing

    status () {
        $KT/test-status $JOB_NAME '{"key":"'kernel.maas.job.status'", "op":"'$1'", '$2'}'
    }

    MAAS=$($KT/maas-image-ids $KT/lab.yaml ${data['series-name']} ${data['sut-arch']})
    status job.started $MAAS

    SSH_OPTIONS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet"
    SUT=${data['sut-name']}

<%
provision = '$KT/provision $SUT'
provision += ' --sut=real --sut-series=%s --sut-arch=%s' % (data['series-name'], data['sut-arch'])
provision += ' --debug --nc'
%>
    # Provision the hardware.
    #
    ${provision} || (cat provisioning.log;status provisioning.failed $MAAS;exit 1)
    status provisioning.succeeded $MAAS

            </command>
        </hudson.tasks.Shell>

    </builders>
    <buildWrappers/>
</project>
<!-- vi:set ts=4 sw=4 syntax=mako expandtab: -->

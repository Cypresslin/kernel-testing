<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties>
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
    KT=/var/lib/jenkins/kernel-testing

    sleep 60
    $KT/iozone-nolazy-results/ingest $JENKINS_HOME/jobs/${data.job_name}/builds/${data.build_id}
            </command>
        </hudson.tasks.Shell>

    </builders>
    <publishers/>
    <buildWrappers/>
</project>
<!-- vi:set ts=4 sw=4 expandtab: -->

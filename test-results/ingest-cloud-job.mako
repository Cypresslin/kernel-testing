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

sleep 10
echo "{ \"repository_root\" : \"$WORKSPACE\" }" > /tmp/$JOB_NAME-results.rc
$KT/test-results/ingest --config=/tmp/$JOB_NAME-results.rc $JENKINS_HOME/jobs/${data.job_name}/builds/${data.build_id}
rsync -arv -e "ssh -A bradf@192.168.1.9 ssh" $WORKSPACE/ jenkins@kernel-jenkins.kernel:metrics/test-results/
$KT/test-results-announce ${data.job_name} $JENKINS_HOME/jobs/${data.job_name}/builds/${data.build_id} || true
            </command>
        </hudson.tasks.Shell>

    </builders>
    <publishers/>
    <buildWrappers/>
</project>
<!-- vi:set ts=4 sw=4 expandtab: -->

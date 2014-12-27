#!/bin/sh

SERIES="precise trusty utopic vivid"
ARCHES="i386 amd64"
HOSTS="rizzo tarf zmeu rainier cavac larsen bantam"
TESTS="qa"

for series in $SERIES; do
    for arch in $ARCHES; do
        for host in $HOSTS; do
            ../jenkins-job-creator/jjc --sut=real --hw=$host --sut-arch=$arch --sut-series=$series --sut-series-decoration=SRU --jenkins-url=http://kernel-jenkins.kernel:8080 --test="$TESTS"
        done
    done
done

for series in $SERIES; do
    for arch in $ARCHES; do
        for host in $HOSTS; do
            ../jenkins-job-creator/jjc --sut=real --hw=$host --sut-arch=$arch --sut-series=$series --sut-series-decoration=SRU --jenkins-url=http://kernel-jenkins.kernel:8080 --sut-hwe --test="$TESTS"
        done
    done
done

for series in trusty utopic vivid; do
    for arch in ppc64el; do
        for host in modoc; do
            ../jenkins-job-creator/jjc --sut=real --hw=$host --sut-arch=$arch --sut-series=$series --sut-series-decoration=SRU --jenkins-url=http://kernel-jenkins.kernel:8080 --test="$TESTS"
        done
    done
done

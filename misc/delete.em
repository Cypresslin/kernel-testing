#!/bin/bash

while read line; do
    echo $line
    ./aka -u http://10.98.2.20:8080 job-delete $line
done <$1

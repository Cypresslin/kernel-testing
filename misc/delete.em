#!/bin/bash

while read line; do
    echo $line
    ./aka  job-delete $line
done <$1

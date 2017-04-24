#!/bin/bash

version="2017-04-24T1830Z"

echo ""$(date "+%Y-%m-%dT%H%MZ" --utc)" run archive loop"

while true; do
    ./run_archive.sh
    echo ""$(date "+%Y-%m-%dT%H%MZ" --utc)" next archive loop in 24 hours"
    sleep 86400
done

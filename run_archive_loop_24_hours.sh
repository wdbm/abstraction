#!/bin/bash

version="2017-04-24T1421Z"

echo ""$(date "+%Y-%m-%dT%H%MZ" --utc)" run archive loop"

while true; do
    ./run_archive.sh
    sleep 86400
done

echo "next archive loop in 24 hours"

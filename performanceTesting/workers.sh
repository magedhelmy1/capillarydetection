#!/bin/bash

set -o monitor

for i in $(seq 0 4); do
    locust -f ./performanceTesting/load_testing.py --worker &
done

while fg; do true; done

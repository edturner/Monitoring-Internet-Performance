#!/bin/bash

# Directory to store logs
LOG_DIR="/storage/ref21gru/CW/logs"
mkdir -p "${LOG_DIR}"

# Current date and time
NOW=$(date +"%Y-%m-%d_%H-%M-%S")

# Targets
TARGETS=("altnews.in" "www.2345.com")

# Loop through each target and run traceroute
for target in "${TARGETS[@]}"; do
    LOG_FILE="${LOG_DIR}/traceroute_${target//./_}_${NOW}.txt"
    echo "Traceroute to $target at $(date)" > "${LOG_FILE}"
    traceroute -n $target >> "${LOG_FILE}" 2>&1
    echo "---------------------------------------------" >> "${LOG_FILE}"
done

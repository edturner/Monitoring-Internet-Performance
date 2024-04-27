#!/bin/bash

# Directory to store logs
LOG_DIR="/storage/knb22bku/"
mkdir -p "${LOG_DIR}"

# Current date and time
NOW=$(date +"%Y-%m-%d_%H-%M-%S")

# Ping targets
PING_TARGETS=("altnews.in" "www.2345.com")

# Loop through each target and run ping commands
for target in "${PING_TARGETS[@]}"; do
    LOG_FILE="${LOG_DIR}/ping_${target//./_}_${NOW}.txt"
    echo "Ping to $target at $(date)" > "${LOG_FILE}"
    ping -c 120 $target >> "${LOG_FILE}" 2>&1  # Send 120 ping packets
    echo "---------------------------------------------" >> "${LOG_FILE}"
done
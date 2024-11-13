#!/bin/bash

# Define the log file
LOG_FILE="./install_script.log"

# Define the source and destination paths
SOURCE_PATH="bin/amd64/ffmpeg"
DESTINATION_PATH="yt-dlp/yt_dlp/ffmpeg"

# Copy the file and force overwrite
echo "Copying ffmpeg..." | tee -a "$LOG_FILE"
cp -f "$SOURCE_PATH" "$DESTINATION_PATH" 2>&1 | tee -a "$LOG_FILE"
echo "ffmpeg has been copied to yt-dlp/yt_dlp and overwritten if it existed." | tee -a "$LOG_FILE"

## --mysql start      if not use docker as mysql server,comment this block
chmod +x docker/docker.sh
# Call the build function from docker.sh
echo "Building Docker images..." | tee -a "$LOG_FILE"
cd ./docker && sh docker.sh build 2>&1 | tee -a "$LOG_FILE"
# Call the up function from docker.sh
echo "Starting Docker containers..." | tee -a "$LOG_FILE"
sh docker.sh up 2>&1 | tee -a "$LOG_FILE"
## --mysql end

## do anaconda install and set crontab
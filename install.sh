#!/bin/bash

# Define the source and destination paths
SOURCE_PATH="bin/amd64/ffmpeg"
DESTINATION_PATH="yt-dlp/yt_dlp/ffmpeg"

# Copy the file and force overwrite
cp -f "$SOURCE_PATH" "$DESTINATION_PATH"

echo "ffmpeg has been copied to yt-dlp/yt_dlp and overwritten if it existed."
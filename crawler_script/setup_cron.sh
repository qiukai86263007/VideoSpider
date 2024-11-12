#!/bin/bash

# Get the absolute path of download_cli.py
SCRIPT_PATH=$(realpath crawler_script/download_cli.py)

# Determine the path to download_cron
CRON_PATH=$(realpath crawler_script/cron/download_cron)

# Write the crontab configuration to download_cron
echo "0 2 * * * /usr/bin/python3 $SCRIPT_PATH" > "$CRON_PATH"

# Install the new crontab
crontab "$CRON_PATH"

echo "Crontab configured to run download_cli.py every day at 2 AM."
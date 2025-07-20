#!/bin/bash

# Simple Cron Setup Script
# Sets up automated data collection and cleansing

echo "Setting up automated data collection and cleansing..."

# Check if scripts exist
if [ ! -f "/home/scripts/data_collection/collect_data.py" ]; then
    echo "Error: Data collection script not found"
    exit 1
fi

if [ ! -f "/home/scripts/data_cleansing/clean_data.py" ]; then
    echo "Error: Data cleansing script not found"
    exit 1
fi

# Create directories
mkdir -p /home/cron
mkdir -p /home/cron/logs

echo "Directories created"

# Backup existing crontab
if crontab -l 2>/dev/null; then
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S)
    echo "Existing crontab backed up"
fi

# Create new crontab entries
crontab -l 2>/dev/null > /tmp/new_crontab

# Add data collection entries (08:00, 12:00, 15:00 WIB)
echo "# Data Collection Script - Runs 3 times daily" >> /tmp/new_crontab
echo "0 8 * * * TZ=Asia/Jakarta /usr/bin/python3 /home/scripts/data_collection/collect_data.py >> /home/cron/logs/cron.log 2>&1" >> /tmp/new_crontab
echo "0 12 * * * TZ=Asia/Jakarta /usr/bin/python3 /home/scripts/data_collection/collect_data.py >> /home/cron/logs/cron.log 2>&1" >> /tmp/new_crontab
echo "0 15 * * * TZ=Asia/Jakarta /usr/bin/python3 /home/scripts/data_collection/collect_data.py >> /home/cron/logs/cron.log 2>&1" >> /tmp/new_crontab

# Add data cleansing entry (daily at 02:00 WIB)
echo "# Data Cleansing Script - Runs daily" >> /tmp/new_crontab
echo "0 2 * * * TZ=Asia/Jakarta /usr/bin/python3 /home/scripts/data_cleansing/clean_data.py >> /home/cron/logs/cron.log 2>&1" >> /tmp/new_crontab

# Install the new crontab
crontab /tmp/new_crontab

# Clean up
rm /tmp/new_crontab

echo "Cron jobs set up successfully"
echo "Data Collection: 08:00, 12:00, 15:00 WIB (daily)"
echo "Data Cleansing: 02:00 WIB (daily)"
echo "Logs will be saved to /home/cron/logs/" 
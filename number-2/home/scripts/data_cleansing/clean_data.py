#!/usr/bin/env python3
"""
Simple Data Cleansing Script
Deletes CSV files older than 30 days.
Runs daily at 02:00 WIB.
"""

import os
import glob
import logging
from datetime import datetime, timezone, timedelta

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cron/logs/cleansing.log'),
        logging.StreamHandler()
    ]
)

def get_wib_time():
    """Get current time in WIB (UTC+7)"""
    utc_time = datetime.now(timezone.utc)
    wib_time = utc_time.astimezone(timezone(timedelta(hours=7)))
    return wib_time

def get_file_age_days(file_path):
    """Get the age of a file in days"""
    try:
        file_stat = os.stat(file_path)
        file_time = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc)
        wib_time = get_wib_time()
        age_delta = wib_time - file_time
        return age_delta.days
    except Exception as e:
        logging.error(f"Error getting file age for {file_path}: {str(e)}")
        return None

def find_old_files(cron_dir, max_age_days=30):
    """Find files older than specified days"""
    old_files = []
    
    if not os.path.exists(cron_dir):
        logging.warning(f"Directory {cron_dir} does not exist")
        return old_files
    
    csv_files = glob.glob(os.path.join(cron_dir, "*.csv"))
    logging.info(f"Found {len(csv_files)} CSV files")
    
    for file_path in csv_files:
        age_days = get_file_age_days(file_path)
        
        if age_days is not None and age_days > max_age_days:
            old_files.append(file_path)
            logging.info(f"File {file_path} is {age_days} days old (will be deleted)")
    
    return old_files

def delete_files(file_list):
    """Delete the specified files"""
    success_count = 0
    failed_count = 0
    
    for file_path in file_list:
        try:
            os.remove(file_path)
            logging.info(f"Deleted: {file_path}")
            success_count += 1
        except Exception as e:
            logging.error(f"Failed to delete {file_path}: {str(e)}")
            failed_count += 1
    
    return success_count, failed_count

def main():
    """Main function"""
    try:
        logging.info("Starting data cleansing")
        
        # Configuration
        cron_dir = "/home/cron"
        max_age_days = 30
        
        # Create directories if they don't exist
        os.makedirs(cron_dir, exist_ok=True)
        os.makedirs('/home/cron/logs', exist_ok=True)
        
        # Find old files
        old_files = find_old_files(cron_dir, max_age_days)
        
        if not old_files:
            logging.info("No old files found to delete")
        else:
            # Delete files
            success_count, failed_count = delete_files(old_files)
            logging.info(f"Cleansing completed: {success_count} deleted, {failed_count} failed")
        
        logging.info("Data cleansing completed")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 
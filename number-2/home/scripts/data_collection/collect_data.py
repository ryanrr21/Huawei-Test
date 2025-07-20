#!/usr/bin/env python3
"""
Simple Data Collection Script
Collects data and saves to CSV files.
Runs at 08:00, 12:00, and 15:00 WIB daily.
"""

import os
import csv
import logging
from datetime import datetime, timezone, timedelta

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/cron/logs/collection.log'),
        logging.StreamHandler()
    ]
)

def get_wib_time():
    """Get current time in WIB (UTC+7)"""
    utc_time = datetime.now(timezone.utc)
    wib_time = utc_time.astimezone(timezone(timedelta(hours=7)))
    return wib_time

def collect_data():
    """Collect data from source"""
    # Sample data - replace with your actual data collection
    data = {
        'timestamp': get_wib_time().isoformat(),
        'temperature': 25.5,
        'humidity': 60.2,
        'pressure': 1013.25,
        'status': 'active'
    }
    return data

def save_to_csv(data, filename):
    """Save data to CSV file"""
    # Create directories if they don't exist
    os.makedirs('/home/cron', exist_ok=True)
    os.makedirs('/home/cron/logs', exist_ok=True)
    
    filepath = f'/home/cron/{filename}'
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        if data:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
    
    logging.info(f'Data saved to {filepath}')

def generate_filename():
    """Generate filename with current date and time"""
    wib_time = get_wib_time()
    date_str = wib_time.strftime("%m%d%Y")
    time_str = wib_time.strftime("%H.%M")
    return f"cron_{date_str}_{time_str}.csv"

def main():
    """Main function"""
    try:
        logging.info("Starting data collection")
        
        # Collect data
        data = collect_data()
        
        # Generate filename
        filename = generate_filename()
        
        # Save data
        save_to_csv(data, filename)
        
        logging.info("Data collection completed")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 
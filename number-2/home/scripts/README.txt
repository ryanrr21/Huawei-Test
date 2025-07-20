Automated Data Collection and Cleansing System

This system provides automated data collection and management through two scripts.

FILES:
- collect_data.py: Collects data 3 times daily (08:00, 12:00, 15:00 WIB)
- clean_data.py: Cleans old files daily (02:00 WIB)
- setup_cron.sh: Sets up cron jobs
- test.py: Tests the system

SETUP:
1. Make scripts executable:
   chmod +x /home/scripts/data_collection/collect_data.py
   chmod +x /home/scripts/data_cleansing/clean_data.py
   chmod +x /home/scripts/setup_cron.sh

2. Run setup script:
   ./setup_cron.sh

3. Test the system:
   python3 test.py

CRON SCHEDULE:
- Data Collection: 08:00, 12:00, 15:00 WIB (daily)
- Data Cleansing: 02:00 WIB (daily)

DATA OUTPUT:
- Files saved to: /home/cron/
- Logs saved to: /home/cron/logs/
- File format: cron_MMDDYYYY_HH.MM.csv

CONFIGURATION:
- Edit collect_data.py to change data collection logic
- Edit clean_data.py to change retention period (default: 30 days)

TESTING:
- Run test.py to verify system works
- Check logs in /home/cron/logs/
- View cron jobs with: crontab -l 
#!/usr/bin/env python3
"""
Simple Test Script
Tests data collection and cleansing scripts.
"""

import os
import subprocess
import sys

def test_collection():
    """Test data collection script"""
    print("Testing data collection script...")
    
    script_path = "/home/scripts/data_collection/collect_data.py"
    
    if not os.path.exists(script_path):
        print("Data collection script not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Data collection script executed successfully")
            return True
        else:
            print(f"Data collection script failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running data collection script: {str(e)}")
        return False

def test_cleansing():
    """Test data cleansing script"""
    print("Testing data cleansing script...")
    
    script_path = "/home/scripts/data_cleansing/clean_data.py"
    
    if not os.path.exists(script_path):
        print("Data cleansing script not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Data cleansing script executed successfully")
            return True
        else:
            print(f"Data cleansing script failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running data cleansing script: {str(e)}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("Checking directories...")
    
    directories = [
        "/home/cron",
        "/home/cron/logs",
        "/home/scripts/data_collection",
        "/home/scripts/data_cleansing"
    ]
    
    all_exist = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"Directory exists: {directory}")
        else:
            print(f"Directory missing: {directory}")
            all_exist = False
    
    return all_exist

def main():
    """Main test function"""
    print("Starting system test...")
    
    # Check directories
    dirs_ok = check_directories()
    
    # Test scripts
    collection_ok = test_collection()
    cleansing_ok = test_cleansing()
    
    print("\nTest Results:")
    print(f"Directories: {'OK' if dirs_ok else 'FAIL'}")
    print(f"Data Collection: {'OK' if collection_ok else 'FAIL'}")
    print(f"Data Cleansing: {'OK' if cleansing_ok else 'FAIL'}")
    
    if dirs_ok and collection_ok and cleansing_ok:
        print("All tests passed")
        return 0
    else:
        print("Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
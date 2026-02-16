#!/usr/bin/env python3
"""
Book Scanner Application
Main entry point for the book scanning application.
Allows users to scan book barcodes and fetch book information.
"""

import sys
from pathlib import Path

# Add project root to path if needed
sys.path.insert(0, str(Path(__file__).parent))

from utils import setup_logger
from data_management import DataManager
import pandas as pd
from barcode_scanner import BarcodeScanner
from configs import Config

# Initialize logger
logger = setup_logger()

def main():
    """Main function with mode selection"""
    logger.info("="*60)
    logger.info("📚 BOOK SCANNER APPLICATION")
    logger.info("="*60)
    
    # Initialize DataManager and setup dataframe
    logger.info("Initializing Data Manager...")
    data_manager = DataManager()
    df = data_manager.setup_dataframe()
    data_manager.display_dataframe_summary(df)
    
    # Initialize BarcodeScanner with the dataframe
    app = BarcodeScanner()
    
    # Mode selection
    print("\n" + "="*50)
    print("📋 SELECT SCANNING MODE")
    print("="*50)
    print("1. 📸 Single scan (test with saved image)")
    print("2. 🎥 Interactive scanner (continuous with webcam)")
    print("3. 📊 View summary only")
    print("4. 🚪 Exit")
    print("="*50)
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == '1':
        logger.info("Starting single scan mode...")
        df = app.single_scan_mode(df)
        
    elif choice == '2':
        logger.info("Starting interactive scanner mode...")
        df = app.interactive_scanner(df)
        
    elif choice == '3':
        logger.info("Displaying current summary...")
        data_manager.display_dataframe_summary(df)
        
    elif choice == '4':
        logger.info("Exiting application...")
        return
    
    else:
        logger.error(f"Invalid choice: {choice}")
        print("Please enter a number between 1 and 4.")
        return
    
    # Save final data if changes were made
    if len(df) > 0:
        logger.info("\n💾 Saving data to Excel...")
        data_manager.save_to_excel(df, Config.EXCEL_FILENAME, mode='append')
        
        logger.info("\n📊 Final Summary:")
        data_manager.display_dataframe_summary(df)
    
    logger.info("👋 Application closed. Happy reading!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
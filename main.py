
from utils import setup_logger
from data_management import setup_dataframe, save_to_excel, display_dataframe_summary
from barcode_scanner import interactive_scanner, single_scan_mode
from configs import Config
logger = setup_logger()



def main():
    """Main function with mode selection"""
    logger.info("="*60)
    logger.info("📚 BOOK SCANNER APPLICATION")
    logger.info("="*60)
    
    # Setup DataFrame
    df = setup_dataframe(Config.EXCEL_FILENAME)
    display_dataframe_summary(df)
    
    # Mode selection
    print("\nSelect mode:")
    print("1. Single scan (test with saved image)")
    print("2. Interactive scanner (continuous with webcam)")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        df = single_scan_mode(df)
    elif choice == '2':
        df = interactive_scanner(df)
    elif choice == '3':
        logger.info("Exiting application...")
        return
    else:
        logger.error("Invalid choice")
        return
    
    # Save final data
    if len(df) > 0:
        save_to_excel(df, Config.EXCEL_FILENAME, mode='append')
        logger.info("\n📊 Final Summary:")
        display_dataframe_summary(df)
    
    logger.info("👋 Application closed")

if __name__ == "__main__":
    main()
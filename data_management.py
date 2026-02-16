
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from datetime import datetime
import os
from tqdm import tqdm
from configs import Config
from utils import setup_logger
from barcode_processing import BarcodeProcessor

logger = setup_logger() 

@dataclass
class DataManager: 
    barcode_processor = BarcodeProcessor()
    
    def setup_dataframe(self) -> pd.DataFrame:
        """Create or load DataFrame from Excel file"""
        filepath = Path(Config.EXCEL_FILENAME)

        if os.path.exists(filepath):
            df = pd.read_excel(filepath)
            logger.info(f"📂 Loaded existing file '{filepath}' with {len(df)} records")
            return df
        else:
            df = pd.DataFrame(columns=[
                "Date Scanned",
                "ISBN",
                "Title",
                "Authors",
                "Publish Date",
                "Categories/Genres",
                "Status"
            ])
            logger.info("📁 Created new DataFrame")
            return df

    def add_books_simple(self, df: pd.DataFrame, isbn_list: list) -> tuple[pd.DataFrame, int]:
        """Add multiple books with duplicate checking"""
        if not isbn_list:
            return df, 0
        
        today_date = datetime.now().strftime("%Y-%m-%d")
        new_records = []
        added_count = 0
        
        # Ensure df is valid
        if df is None or not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(columns=[
                "Date Scanned", "ISBN", "Title", "Authors", 
                "Publish Date", "Categories/Genres", "Status"
            ])
        
        # Get existing ISBNs
        existing_isbns = set()
        if len(df) > 0 and 'ISBN' in df.columns:
            existing_isbns = set(df['ISBN'].astype(str).str.upper())

        for isbn in tqdm(isbn_list, desc="📖 Processing books", unit="book"):        
            if isbn.upper() in existing_isbns:
                logger.info(f"⏭️  Skipping duplicate ISBN: {isbn}")
                continue    # Check duplicate
                if isbn.upper() in existing_isbns:
                    logger.info(f"⏭️  Skipping duplicate ISBN: {isbn}")
                    continue
                
            logger.info(f"📖 Processing new ISBN: {isbn}")
            book_info = self.barcode_processor.get_book_info(isbn)
                
            # Show which book was added
            if book_info.get("title") != "N/A":
                logger.info(f"✨ Added: {book_info['title']} by {book_info['authors']}")
            else:
                logger.info(f"✨ Added ISBN: {isbn} (details not found)")
            
            new_records.append({
                "Date Scanned": today_date,
                "ISBN": isbn,
                "Title": book_info.get("title", "N/A"),
                "Authors": book_info.get("authors", "N/A"),
                "Publish Date": book_info.get("publish_date", "N/A"),
                "Categories/Genres": book_info.get("categories", "N/A"),
                "Status": "Found" if book_info.get("title") != "N/A" else "Not Found"
            })
            
            existing_isbns.add(isbn.upper())
            added_count += 1
            
        if new_records:
            new_df = pd.DataFrame(new_records)
            df = pd.concat([df, new_df], ignore_index=True)
            logger.info(f"✅ Added {added_count} new book(s) to DataFrame")
        else:
            logger.info("📋 No new books to add")
        
        return df, added_count

    def save_to_excel(self, df: pd.DataFrame, filepath=Config.EXCEL_FILENAME, mode='append') -> bool:
        """Save DataFrame to Excel"""
        try:
            if not isinstance(df, pd.DataFrame):
                logger.error(f"Expected DataFrame, got {type(df)}")
                return False
        
        
            if mode == 'append' and os.path.exists(filepath):
                existing_df = pd.read_excel(filepath)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=['ISBN'], keep='last')
                combined_df.to_excel(filepath, index=False)
                logger.info(f"✅ Appended to '{filepath}' - Total records: {len(combined_df)}")
            else:
                df.to_excel(filepath, index=False)
                logger.info(f"✅ Saved to '{filepath}' - Total records: {len(df)}")
            
            return True
        except Exception as e:
            logger.error(f"Error saving to Excel: {e}")
            return False

    def display_dataframe_summary(self, df: pd.DataFrame):
        """Display DataFrame summary - shows unique books only (simple version)"""
        if len(df) == 0:
            logger.info("📊 DataFrame is empty")
            return
        
        logger.info("\n" + "="*50)
        logger.info("📊 DATAFRAME SUMMARY")
        logger.info("="*50)
        logger.info(f"Total Scans: {len(df)}")
        
        # Show unique books scanned today
        today = datetime.now().strftime("%Y-%m-%d")
        today_scans = df[df['Date Scanned'] == today]
        if len(today_scans) > 0:
            # Get unique books from today's scans
            unique_today = today_scans.drop_duplicates(subset=['ISBN'], keep='first')
            
            logger.info("\n📅 Books scanned today:")
            for _, row in unique_today.iterrows():
                logger.info(f"  • {row['Title']}")


        logger.info("="*50)


import cv2
import numpy as np
import pandas as pd
from data_management import save_to_excel, add_books_simple, display_dataframe_summary
from configs import Config
from utils import setup_logger
from barcode_processing import decode_barcodes, take_barcode_image
logger = setup_logger()



def interactive_scanner(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interactive scanner that allows continuous scanning
    Press SPACE to capture and scan, 'q' to quit
    """
    logger.info("Starting interactive scanner...")
    logger.info("Press SPACE to capture and scan barcode")
    logger.info("Press 'q' to quit")
    
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        logger.error("Failed to open camera")
        return df
    
    scanned_count = 0
    
    while True:
        # Show live preview
        ret, frame = capture.read()
        if not ret:
            logger.error("Failed to capture frame")
            break
        
        # Add instructions to frame
        cv2.putText(frame, "Press SPACE to scan, 'q' to quit", 
                   (10, 30), Config.FONT, 0.7, Config.WHITE, 2)
        cv2.putText(frame, f"Scanned this session: {scanned_count}", 
                   (10, 60), Config.FONT, 0.6, Config.GREEN, 2)
        
        cv2.imshow(Config.PREVIEW_WINDOW, frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # SPACE key
            logger.info("📸 Capturing image...")
            
            # Capture frame
            ret, captured_frame = capture.read()
            if ret:
                # Save captured image
                cv2.imwrite(Config.TEST_IMAGE, captured_frame)
                
                # Decode barcodes
                result = decode_barcodes(captured_frame)
                
                if result is None:
                    logger.warning("Failed to decode barcodes")
                    continue
                
                isbn_list, marked_frame = result
                
                if isbn_list:
                    # Show detected ISBNs
                    cv2.imshow("Detected Barcodes", marked_frame)
                    cv2.waitKey(2000)  # Show for 2 seconds
                    cv2.destroyWindow("Detected Barcodes")
                    

                    # Add to database
                    result = add_books_simple(df, isbn_list)

                    added = 0
                    if result is not None:
                        df, added = result
                        scanned_count += added
                        
                        # Show success message
                        success_frame = np.zeros((200, 600, 3), dtype=np.uint8)
                        cv2.putText(success_frame, f"✅ Added {added} new book(s)!", 
                                (50, 100), Config.FONT, 1, Config.GREEN, 2)
                        cv2.imshow("Success", success_frame)
                        cv2.waitKey(1500)
                        cv2.destroyWindow("Success")
                    else:
                        logger.warning("No ISBN found in image")
                        
                        # Show error message
                        error_frame = np.zeros((200, 600, 3), dtype=np.uint8)
                        cv2.putText(error_frame, "❌ No ISBN detected", 
                                (50, 100), Config.FONT, 1, Config.RED, 2)
                        cv2.putText(error_frame, "Try again with a clear barcode", 
                                (50, 150), Config.FONT, 0.7, Config.WHITE, 1)
                        cv2.imshow("Error", error_frame)
                        cv2.waitKey(1500)
                        cv2.destroyWindow("Error")
                else:
                    logger.error("Failed to capture image")
            
        elif key == ord('q'):  # Quit
            logger.info("Exiting interactive scanner...")
            break
    
    capture.release()
    cv2.destroyAllWindows()
    return df


def single_scan_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Single scan mode (original functionality)"""
    logger.info("Starting single scan mode...")
    
    image = take_barcode_image(dev_mode=True)
    

    if image is not None:
        result = decode_barcodes(image)
        
        if result is None:
            logger.error("Failed to decode barcodes.")
            return df
        
        isbn_list, marked_frame = result
        
        if isbn_list:
            # Show marked image
            cv2.imshow("Detected Barcodes", marked_frame)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
            
            result = add_books_simple(df, isbn_list)
            
            if result is not None:
                df, added = result
                if added > 0:
                    save_to_excel(df, Config.EXCEL_FILENAME, mode='append')
                    display_dataframe_summary(df)
            else:
                logger.info("No new books to add.")
        else:
            logger.warning("No ISBNs found in the image.")
    else:
        logger.error("No image captured.")
    
    return df

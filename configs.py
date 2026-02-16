
import cv2

class Config:
    EXCEL_FILENAME = "book_scans.xlsx"
    TEST_IMAGE = "barcode_image.png"
    WINDOW_NAME = "Book Scanner - Press SPACE to scan, 'q' to quit"
    PREVIEW_WINDOW = "Camera Preview"
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    WHITE = (255, 255, 255)
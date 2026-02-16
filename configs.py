
import cv2
from dataclasses import dataclass
import numpy as np
from typing import  Dict, Any

@dataclass
class Config:
    EXCEL_FILENAME: str = "book_scans.xlsx"
    TEST_IMAGE: str = "barcode_image.png"
    WINDOW_NAME: str = "Book Scanner - Press SPACE to scan, 'q' to quit"
    PREVIEW_WINDOW: str = "Camera Preview"
    FONT: int = cv2.FONT_HERSHEY_SIMPLEX
    GREEN: tuple = (0, 255, 0)
    RED: tuple = (0, 0, 255)
    BLUE: tuple = (255, 0, 0)
    WHITE: tuple = (255, 255, 255)


@dataclass
class BookInfo:
    title: str
    authors: str
    publish_date: str
    categories: str

    @property
    def is_found(self) -> bool:
        return self.title != "N/A"


@dataclass
class ScanResult:
    isbn_list: list[str]
    frame_with_boxes: np.ndarray


@dataclass
class DataRecord:
    date_scanned: str
    isbn: str
    title: str
    authors: str
    publish_date: str
    categories: str
    status: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "Date Scanned": self.date_scanned,
            "ISBN": self.isbn,
            "Title": self.title,
            "Authors": self.authors,
            "Publish Date": self.publish_date,
            "Categories/Genres": self.categories,
            "Status": self.status
        }
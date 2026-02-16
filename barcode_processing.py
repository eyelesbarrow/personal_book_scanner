import re
import time
from dataclasses import dataclass

import cv2
import numpy as np
import requests
from pyzbar.pyzbar import decode

from configs import Config
from utils import setup_logger

logger = setup_logger()


@dataclass
class BarcodeProcessor:
    """Class to handle barcode scanning and book information retrieval
    Takes barcode image, decodes it, checks if it's an ISBN, and fetches book info from Open Library API
    Returns list of ISBNs and annotated image with detected barcodes
    """

    def take_barcode_image(self, dev_mode=False) -> np.ndarray | None:
        """Capture barcode from webcam or use saved image"""
        if dev_mode:
            logger.info("Developer mode enabled: Skipping webcam capture.")
            barcode_frame = cv2.imread(Config.TEST_IMAGE)
            if barcode_frame is None:
                logger.error(
                    f"Failed to load '{Config.TEST_IMAGE}'. Please ensure the file exists."
                )
                return None
            return barcode_frame

        else:
            logger.info("Starting webcam capture...")
            capture = cv2.VideoCapture(0)
            time.sleep(1)

            ret, barcode_frame = capture.read()

            if ret:
                cv2.imwrite(Config.TEST_IMAGE, barcode_frame)
                logger.info(f"Image captured and saved as '{Config.TEST_IMAGE}'.")
            else:
                logger.error("Failed to capture image from webcam.")
                return None

            capture.release()
            return barcode_frame

    def decode_barcodes(
        self, barcode_frame: np.ndarray
    ) -> tuple[list, np.ndarray] | None:
        """Decode barcodes from image"""
        if barcode_frame is None:
            logger.error("No barcode image to decode.")
            return None

        gray_barcode = cv2.cvtColor(barcode_frame, cv2.COLOR_BGR2GRAY)
        decoded_barcodes = decode(barcode_frame)

        if not decoded_barcodes:
            decoded_barcodes = decode(gray_barcode)
            if decoded_barcodes:
                logger.debug("Barcode detected in grayscale image")

        isbn_list = []
        frame_with_boxes = barcode_frame.copy()

        for each_barcode in decoded_barcodes:
            barcode_data = each_barcode.data.decode("utf-8")
            barcode_type = each_barcode.type

            logger.info(f"Decoded Barcode: {barcode_data}")
            logger.info(f"Barcode Type: {barcode_type}")

            if self.is_isbn(barcode_data):
                isbn_list.append(barcode_data)
                logger.info(f"✅ ISBN Detected: {barcode_data}")

                # Draw green box for ISBN
                points = each_barcode.polygon
                if len(points) == 4:
                    pts = [(point.x, point.y) for point in points]
                    pts = np.array(pts, dtype=np.int32)
                    cv2.polylines(frame_with_boxes, [pts], True, Config.GREEN, 3)

                    # Add background for text
                    text = f"ISBN: {barcode_data}"
                    text_size = cv2.getTextSize(text, Config.FONT, 0.6, 2)[0]
                    cv2.rectangle(
                        frame_with_boxes,
                        (pts[0][0], pts[0][1] - 25),
                        (pts[0][0] + text_size[0] + 10, pts[0][1] - 5),
                        Config.GREEN,
                        -1,
                    )
                    cv2.putText(
                        frame_with_boxes,
                        text,
                        (pts[0][0] + 5, pts[0][1] - 10),
                        Config.FONT,
                        0.6,
                        Config.WHITE,
                        2,
                    )
            else:
                # Draw red box for non-ISBN barcodes
                points = each_barcode.polygon
                if len(points) == 4:
                    pts = [(point.x, point.y) for point in points]
                    pts = np.array(pts, dtype=np.int32)
                    cv2.polylines(frame_with_boxes, [pts], True, Config.RED, 2)
                    cv2.putText(
                        frame_with_boxes,
                        "Not ISBN",
                        (pts[0][0], pts[0][1] - 10),
                        Config.FONT,
                        0.5,
                        Config.RED,
                        2,
                    )

        return isbn_list, frame_with_boxes

    def is_isbn(self, barcode_data: str) -> bool:
        """Check if barcode data matches ISBN format"""
        cleaned = re.sub(r"[^0-9X]", "", barcode_data.upper())

        # ISBN-13
        if (
            len(cleaned) == 13
            and cleaned.isdigit()
            and cleaned.startswith(("978", "979"))
        ):
            return True

        # ISBN-10
        if len(cleaned) == 10:
            if cleaned[:9].isdigit() and (cleaned[9].isdigit() or cleaned[9] == "X"):
                return True

        return False

    def get_book_info(self, isbn: str) -> dict:
        """Fetch book information from Open Library API"""
        try:
            logger.debug(f"Fetching book info for ISBN: {isbn}")
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = requests.get(url, timeout=10)
            data = response.json()

            book_key = f"ISBN:{isbn}"
            if book_key in data:
                book_info = data[book_key]
                title = book_info.get("title", "N/A")

                # Handle authors
                authors_list = book_info.get("authors", [])
                if authors_list:
                    authors = ", ".join(
                        [author.get("name", "Unknown") for author in authors_list]
                    )
                else:
                    authors = "N/A"

                publish_date = book_info.get("publish_date", "N/A")

                # Get subjects/categories
                subjects = book_info.get("subjects", [])
                if subjects:
                    categories = [
                        s.get("name", str(s)) if isinstance(s, dict) else str(s)
                        for s in subjects[:3]
                    ]
                    categories_str = ", ".join(categories)
                    logger.info(f"Categories found: {categories_str}")
                else:
                    categories_str = "N/A"

                logger.info(f"Book found: {title} by {authors}")

                return {
                    "title": title,
                    "authors": authors,
                    "publish_date": publish_date,
                    "categories": categories_str,
                }

            else:
                logger.warning(f"No information found for ISBN {isbn}")
                return {
                    "title": "N/A",
                    "authors": "N/A",
                    "publish_date": "N/A",
                    "categories": "N/A",
                }

        except requests.exceptions.Timeout:
            logger.error("API request timeout")
            return {
                "title": "N/A",
                "authors": "N/A",
                "publish_date": "N/A",
                "categories": "N/A",
            }
        except Exception as e:
            logger.error(f"Error fetching book information: {e}")
            return {
                "title": "N/A",
                "authors": "N/A",
                "publish_date": "N/A",
                "categories": "N/A",
            }

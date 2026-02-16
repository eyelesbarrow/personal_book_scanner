# 📚 Book Scanner Application

A Python-based application that scans book ISBNs using your webcam and automatically fetches book information from the Open Library API, storing the data in an Excel spreadsheet.

This is my personal project. 

## Features

- **📸 Barcode Scanning**: Real-time barcode detection using OpenCV and pyzbar
- **🎥 Multiple Scanning Modes**:
  - Interactive scanner: Continuous scanning with webcam feed
  - Single scan mode: Test mode using saved images
- **📖 Book Information Retrieval**: Automatically fetches book details (title, authors, publication date, categories) from Open Library API
- **📊 Excel Export**: Saves scanned books to an organized Excel file with duplicate prevention
- **⚡ Real-time Feedback**: Visual indicators for successful scans and error states
- **📝 Comprehensive Logging**: Detailed logs with daily log file rotation

## Requirements

- **Python 3.12 or higher**
- Webcam (for interactive scanning)
- Internet connection (for API queries)

## Installation

### 1. Clone or Download the Project
```bash
cd /path/to/book_scan
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `opencv-python` - Computer vision and barcode detection
- `pyzbar` - Barcode decoding
- `pandas` - Data manipulation and Excel handling
- `openpyxl` - Excel file support
- `requests` - HTTP requests for API calls
- `tqdm` - Progress bars

## Configuration

Edit [configs.py](configs.py) to customize settings:

```python
EXCEL_FILENAME = "book_scans.xlsx"  # Output Excel file name
TEST_IMAGE = "barcode_image.png"    # Temporary image for testing
PREVIEW_WINDOW = "Camera Preview"   # Window titles for webcam display
```

## Usage

### Start the Application
```bash
python3 main.py
```

### Menu Options

**1. Single Scan (Test Mode)**
- Uses a saved test image to demonstrate barcode scanning
- Ideal for testing without a webcam
- Requires a `barcode_image.png` file in the project folder

**2. Interactive Scanner (Live Webcam)**
- Opens a live camera feed
- Press **SPACE** to capture and scan a barcode
- Press **Q** to quit and save
- Real-time feedback displayed on screen

**3. Exit**
- Closes the application

### Workflow

1. Launch application → see DataFrame summary
2. Choose scanning mode
3. Scan books using your preferred method
4. Application fetches book details from Open Library API
5. Data is automatically saved to Excel file with:
   - Date Scanned
   - ISBN
   - Title
   - Authors
   - Publication Date
   - Categories/Genres
   - Status (Found/Not Found)

## Project Structure

```
book_scan/
├── main.py                    # Application entry point
├── barcode_scanner.py         # Camera and interactive scanning logic
├── barcode_processing.py      # Barcode detection and ISBN validation
├── data_management.py         # Excel file handling and data operations
├── configs.py                 # Configuration settings
├── utils.py                   # Logging setup
├── book_scans.xlsx           # Generated Excel output
├── logs/                      # Daily log files
└── README.md                  # This file
```

## File Descriptions

| File | Purpose |
|------|---------|
| [main.py](main.py) | Entry point; handles mode selection and workflow |
| [barcode_scanner.py](barcode_scanner.py) | Webcam capture, interactive scanner UI |
| [barcode_processing.py](barcode_processing.py) | Barcode decoding, ISBN validation, API queries |
| [data_management.py](data_management.py) | DataFrame creation, Excel I/O, duplicate handling |
| [configs.py](configs.py) | Color constants and file paths |
| [utils.py](utils.py) | Logging configuration |

## How It Works

### ISBN Detection
1. Barcode is captured from webcam or image
2. `pyzbar` decodes the barcode data
3. Regex validation checks for ISBN-10 or ISBN-13 format
4. Green box drawn around valid ISBNs, red box for invalid barcodes

### Book Information Retrieval
1. Valid ISBN is sent to Open Library API
2. API returns book metadata (if available)
3. Data fields are extracted or marked as "N/A" if unavailable
4. Book is added to DataFrame

### Duplicate Prevention
- Each ISBN is checked against existing records
- Duplicate ISBNs are skipped (new metadata overwrites old on append)
- Prevents accidental duplicate entries

## Logging

Logs are stored in the `logs/` directory with daily rotation:
- **Log Format**: `YYYY-MM-DD_HH:MM:SS - LEVEL - MESSAGE`
- **Console Output**: WARNING level and above
- **File Output**: DEBUG level and above (comprehensive)

Example log file: `logs/book_scanner_20260216.log`

## Troubleshooting

### "Failed to open camera"
- Ensure webcam is connected and not in use by another application
- Check camera permissions in system settings
- Try unplugging and reconnecting the webcam

### "No information found for ISBN"
- Check ISBN format (10 or 13 digits)
- Some older or rare books may not be in Open Library database
- Verify barcode is clearly visible and straight

### Excel file permission error
- Close the Excel file if it's open
- Ensure the file isn't locked by another process

### API timeout errors
- Check your internet connection
- Open Library API may be temporarily unavailable
- Logs will show detailed error messages

## Known Issues

⚠️ **Important**: There are some improvements and features that needs to be done: 
1. testing
2. retry mechanisms
3. better GUI or a web UI dashboard
4. migrate to either poetry or uv
5. CSV option 
6. Export option from csv or excel


These should be addressed in the next update.


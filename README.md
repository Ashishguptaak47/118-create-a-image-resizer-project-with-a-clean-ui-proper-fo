# Image Resizer Application

A modern, clean, and flexible Python application for single and batch image resizing with an intuitive GUI (Tkinter) and CLI support.

## Features

- **Batch Image Resizing**: Process multiple images at once.
- **Flexible Resize Modes**: Resize by exact dimensions (Width x Height) or scale by Percentage.
- **Aspect Ratio Preservation**: Option to maintain aspect ratio automatically.
- **Format Conversion**: Convert images to JPEG, PNG, WEBP, or BMP on export.
- **Quality Control**: Adjust compression quality for JPEG and WEBP formats.
- **Non-blocking UI**: Asynchronous processing with modern Tkinter styling and live progress tracking.
- **CLI Mode**: Run headlessly from command line for automation.

## Project Structure

```
. 
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── app/
│   ├── __init__.py
│   ├── resizer.py
│   └── ui.py
└── tests/
    ├── test_main.py
    └── test_resizer.py
```

## Installation

1. Install Python 3.8 or higher.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Launch GUI Application
Run `main.py` without arguments:
```bash
python main.py
```

### CLI Usage
Run `main.py` with the `--cli` flag:
```bash
python main.py --cli --files image1.jpg image2.png --out ./resized --scale 50 --format WEBP
```

Options:
- `--files`: List of input file paths
- `--out`: Destination directory
- `--width`: Target width in pixels
- `--height`: Target height in pixels
- `--scale`: Scaling percentage (e.g. 50 for 50% scale)
- `--format`: Output format (JPEG, PNG, WEBP, BMP)

## Running Tests

Run tests using `pytest`:
```bash
pytest tests/
```

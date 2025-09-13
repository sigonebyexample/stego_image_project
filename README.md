# stego_image_project
Steganography is the practice of concealing a message within another message or a physical object that is not secret. This project provides a Python implementation of steganography techniques for hiding secret messages within image files using the Least Significant Bit (LSB) method.

# The tool allows you to:

    Encode secret text messages into images

    Decode hidden messages from steganographic images

    Maintain image visual quality while hiding information

    Support various image formats (PNG, BMP, JPEG)

## Features
- LSB Steganography: Hide data in the least significant bits of image pixels
- Multi-format Support: Work with various image formats including PNG, JPEG, and BMP
- Preserved Image Quality: Minimal visual impact on carrier images
- CLI and API Support: Use via command line or import as a Python module
- Metadata Protection: Maintain original image metadata during encoding/decoding
- Batch Processing: Process multiple images simultaneously

## Installation

git clone https://github.com/sigonebyexample/stego_image_project.git
cd stego_image_project

## Install dependencies
pip install -r requirements.txt

## Usage
python sego.py

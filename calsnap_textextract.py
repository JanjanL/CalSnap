import easyocr
import os

def text_extract(screencap: str):
    """
    Extract text from an image using EasyOCR.
    - screencap: path to image file.
    """

    # 1) Check path
    if not os.path.exists(screencap):
        raise FileNotFoundError(f"Image not found: {screencap}")
    
    # 3) Initialize reader (Traditional Chinese + English)
    reader = easyocr.Reader(['ch_tra', 'en'])
    
    # 4) Read text: detail=0 returns a list of strings only
    ocr_result = reader.readtext(screencap, detail=0)
    return ocr_result
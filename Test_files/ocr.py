import pytesseract
from PIL import Image


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))
    return text


text_of_the_document = ocr_core('img/img6.jpg')
print(text_of_the_document)

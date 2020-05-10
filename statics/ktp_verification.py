from dotenv import load_dotenv
import cv2.cv2 as cv2
import pytesseract
import numpy as np
from pytesseract import Output

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def id_verification(filepath):
    try:
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

        res = {}
        result = pytesseract.image_to_string(threshed)
        for word in result.split("\n"):
            # normalize NIK
            if "NIK" in word:
                nik_char = word.split()
                if "D" in word:
                    word = word.replace("D", "0")
                if "?" in word:
                    word = word.replace("?", "7")
                if "b" in word:
                    word = word.replace("b", "6")
            kata = " ".join(word.split())
            if ">" in kata and ":" not in kata:
                data = kata.split('>')
                res[data[0].strip()] = data[1].strip()
            if ":" in kata and ">" not in kata:
                data = kata.split(':')
                res[data[0].strip()] = data[1].strip()
            if "-" in kata and ">" not in kata and ":" not in kata:
                data = kata.split('-')
                res[data[0].strip()] = data[1].strip()
        ret = {
            'status': 200,
            'message': "Extracted Data",
            'results': res
        }
        return ret
    except Exception as e:
        ret = {
            'status': 500,
            'message': e.args
        }
        return ret

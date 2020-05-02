from dotenv import load_dotenv
import cv2.cv2 as cv2
import pytesseract

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'


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

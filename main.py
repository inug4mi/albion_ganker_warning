import pyautogui
import time
from PIL import ImageGrab
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np
import winsound
import pytesseract # image number detector
import pyttsx3 # text-to-speech

# On my screen
# PK number image position is on
# Point(x=1560, y=1032)
# Point(x=1582, y=1054)

class GankDetector:
    def __init__(self):
        self.imagePos = (1563, 1033, 1590, 1051) # adjust it for better fitting
        number1 = Image.open("./Figure_1.png")
        self.gankerBarPath = './gankerBar.png' 
        self.numberOneImageArray = np.array([[255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,0,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,0,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
 [255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255],
[255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255
 ,255,255,255,255,255,255,255,255,255]])
        self.engine = pyttsx3.init()
        self.current_pk_number = -1 # -1 is equals to None

    def screenshotNumber(self):
        # screenshot on number based on screen coordinates
        screenshot = ImageGrab.grab(bbox=self.imagePos)
        #screenshot.show(screenshot)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def cleanScreenshot(self, image):
        # image processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0,255, cv2.THRESH_OTSU)
        blurred = cv2.medianBlur(binary, 1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
        pimage = cv2.dilate(blurred, kernel, iterations=1)
        pimage = cv2.erode(pimage, kernel, iterations=1)
        # show image
        #plt.imshow(pimage[:,:12])
        #plt.show()

        # for only one digit
        if np.sum(binary[:,12:]) != 0:
            return pimage
        #,2 digits (full image) 99<=PK
        #return pimage
        return pimage[:,:12]

    # image number detection
    def detectNumberOfGankers(self, image):
        # Remember to download and install tesseract
        try:
            tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # directory of tesseract
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        except Exception as e:
            print(f"Install or set correct path for tesseract")
            return e
        # try detecting only single char numbers
        config = '--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'
        try:
            if np.array_equal(image, self.numberOneImageArray):
                text = '1'
            else:
                text = pytesseract.image_to_string(image, config=config)
                text = text.strip()
            print(f"PK: {text}")
            return text
        except Exception as e:
            print("tesseract-OCR error: {e}")
            return ""
            
    def speakNumber(self, number):
        #winsound.Beep(5000, 467)
        self.engine.say(f"There are {number} PK")
        self.engine.runAndWait()

    def setPKNumber(self, new_number):
        if self.isValidNumber(new_number):
            self.current_pk_number = new_number
    # checks if the number has changed
    def updatePKNumber(self, new_number):
        return (self.isValidNumber(new_number) and (new_number != self.current_pk_number))

    def isValidNumber(self, number):
        return number.isdigit()

if __name__ == '__main__':
    time.sleep(1.5)
    gankDetector = GankDetector()
    # repeat over and over again
    while True:
        #gankDetector.isGanekrClose()
        image = gankDetector.screenshotNumber()
        clean_image = gankDetector.cleanScreenshot(image=image)
        number = gankDetector.detectNumberOfGankers(image=clean_image)
        if gankDetector.updatePKNumber(number):
            gankDetector.speakNumber(number)
            gankDetector.setPKNumber(number)
        # repeats every 0.8 seconds
        time.sleep(0.8)

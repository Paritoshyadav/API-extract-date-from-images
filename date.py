# -*- coding: utf-8 -*-
import pickle
from flask import Flask
import pytesseract
from PIL import Image
import os
import sys
import cv2
import numpy as np
from skimage.filters import threshold_local
import imutils
from imutils.perspective import four_point_transform
from date_extractor import extract_date



def simpleocr(filename):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = str(((pytesseract.image_to_string(Image.open(filename)))))
    date, precision = extract_date(text, return_precision=True)

    return str(date)
    #return clean_text
    


def hybridocr(filename):
    
    image = cv2.imread(filename)
    ratio = image.shape[0]/500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            print(screenCnt.shape)
            break
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
 
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255

    import random
#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
    n=random.randint(1,100)
    image_name=f'imagee{n}.png'
    print(image_name)
    cv2.imwrite(image_name, imutils.resize(warped, height = 650))




    text = str(((pytesseract.image_to_string(Image.open(image_name)))))
    

    date, precision = extract_date(text, return_precision=True)

    return str(date)










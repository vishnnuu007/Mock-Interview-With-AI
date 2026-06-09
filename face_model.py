from database import *
from flask import *
import demjson3 as demjson

import numpy as np
from model_manager import Model
import pickle
import math
import cv2
import uuid

import face_recognition

import argparse

from imutils import paths
import os
import requests
import io
import json
from database import *
from datetime import datetime


def enf(path):
    imagePaths = path
    knownEncodings = []
    knownNames = []
    
    for fname in os.listdir(imagePaths):
        facedir = os.path.join(imagePaths, fname)
        for imagePt in os.listdir(facedir):
            img = os.path.join(facedir, imagePt)
            
            # Verify if the image was successfully read
            image = cv2.imread(img)
            if image is None:
                print(f"[ERROR] Could not read image: {img}")
                continue
            
            print("[INFO] processing image {}/{}".format(fname, len(imagePt)))
            print("imagepath-------", imagePaths)

            name = fname
            
            # Convert the image from BGR (OpenCV format) to RGB
            try:
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except Exception as e:
                print(f"[ERROR] Could not convert image {img} to RGB: {e}")
                continue

            # Detect the face locations in the image
            try:
                boxes = face_recognition.face_locations(rgb, model='hog')
            except Exception as e:
                print(f"[ERROR] Could not detect faces in image {img}: {e}")
                continue

            # Compute the facial encodings
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

    # Serialize the facial encodings and names
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open('faces.pickles', "wb") as f:
        f.write(pickle.dumps(data))

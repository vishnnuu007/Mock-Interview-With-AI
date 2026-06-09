from flask import *
import tensorflow as tf
import keras
import cv2
from keras.models import model_from_json # type: ignore
from keras.preprocessing import image # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator


import numpy as np


import face_recognition
import pickle
from datetime import datetime

from database import *
import tensorflow as tf
from keras.models import Sequential # type: ignore



from email.mime.text import MIMEText
import random
import smtplib
import string


import smtplib
from email.mime.text import MIMEText


# Build and train your Keras model

# OpenCV-related code


model = model_from_json(open(r"model\facial_expression_model_structure.json", "r").read())
model.load_weights(r'model\facial_expression_model_weights.h5')  # load weights



face_cascade = cv2.CascadeClassifier(r'model\haarcascade_frontalface_default.xml')

# ... add layers to the model



# Clear the Keras session


cap = cv2.VideoCapture(0)



emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')


def rec_face_image(imagepath):
    print(imagepath)

    data = pickle.loads(open('faces.pickles', "rb").read())

    # load the input image and convert it from BGR to RGB
    image = cv2.imread(imagepath)
    #print(image)
    h,w,ch=image.shape
    print(ch)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb,
        model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding,tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:

                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            print(counts, " rount ")
            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            if len(counts) == 1:
                name = max(counts, key=counts.get)
            else:
                name = "-1"
        # update the list of names
        # if name not in names:
        if name != "Unknown":
            names.append(name)
    return names

def camclick(s):

    print(s,"/////////ss")
   

    # i=0
    cap = cv2.VideoCapture(0)

    # emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    # model = model_from_json(open(r"model\facial_expression_model_structure.json", "r").read())
    # model.load_weights(r'model\facial_expression_model_weights.h5')

    # face_cascade = cv2.CascadeClassifier(r'model\haarcascade_frontalface_default.xml')

    while True:
        ret, img = cap.read()

        if not ret or img is None:
            print("Error: Unable to capture frame.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            detected_face = img[int(y):int(y+h), int(x):int(x+w)]
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)
            detected_face = cv2.resize(detected_face, (48, 48))
            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

        #     predictions = model.predict(img_pixels)
        #     max_index = np.argmax(predictions[0])
        #     emotion = emotions[max_index]
        #     cv2.putText(img, emotion, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            FaceFileName = "static/test.jpg"
            cv2.imwrite(FaceFileName, detected_face)

            val = rec_face_image(FaceFileName)
            print("VAL............", val)
            print("user", val)
            str1 = ""

            if val:

                if str(s)==str(val[0]):

                
                    for ele in val:
                        q = "select * from user where user_id='%s'" % (ele)
                        res = select(q)
                        print("////////////////////////////////", res)

                        if res:
                            return ("<script>alert('Face Recognized');window.location='/role_selection'</script>")
                        # else:
                        #     return ("<script>alert('Invalid User');window.location='/userhome'</script>")
                                
            #     else:
            #         return ("<script>alert('Invalid User');window.location='/userhome'</script>")
            # else:
            #         return ("<script>alert('Invalid User');window.location='/userhome'</script>")



        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture resources
    cap.release()
    cv2.destroyAllWindows()

    # Clear Keras session
    tf.keras.backend.clear_session()
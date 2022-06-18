from calendar import c
from keras import models
import numpy as np
import cv2
from datetime import datetime

import time
from WebScraper import WebScraper


def drawing_rectangles(grey, faces):
    for (x, y, w, h) in faces:
        # defining the ROI for the color and grey frame
        roi_grey = grey[y : y + h, x : x + w]
        roi_clor = frame[y : y + h, x : x + w]
        img_item = "img.png"
        cv2.imwrite(img_item, roi_grey)

        # drawing rectangle around the ROI
        color = (255, 0, 0)
        stroke = 2
        width = x + w
        height = y + h
        cv2.rectangle(frame, (x, y), (width, height), color, stroke)


# loading in keras model
model = models.load_model("keras_model.h5")
face_cascade = cv2.CascadeClassifier("data\haarcascade_frontalface_alt2.xml")


# Opening label file and storing label values into an array
labelsfile = open("labels.txt", "r")

classes = []
line = labelsfile.readline()
while line:
    classes.append(line.split(" ", 1)[1].rstrip())
    line = labelsfile.readline()
labelsfile.close()

cap = cv2.VideoCapture(0)

# setting the demensions of the frame
frameWidth = 980
frameHeight = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
cap.set(cv2.CAP_PROP_GAIN, 0)


# player region dictionary
WebScrp = WebScraper()

while True:
    # capture from by frame
    rect, frame = cap.read()

    # Defining a np array to store image from frame
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    margin = int(((frameWidth - frameHeight) / 2))
    square_frame = frame[0:frameHeight, margin : margin + frameHeight]
    # resize to 224x224 for use with TM model
    resized_img = cv2.resize(square_frame, (224, 224))
    # convert image color to go to model
    model_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    # turn the image into a numpy array
    image_array = np.asarray(model_img)
    # normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # load the image into the array
    data[0] = normalized_image_array

    # run the prediction
    predictions = model.predict(data)
    print(predictions)
    index_max = np.argmax(predictions[0])
    conformation_thres = 85
    if predictions[0][index_max] * 100 >= conformation_thres:
        vaild = True
        font = cv2.FONT_HERSHEY_SIMPLEX
        name = "this is " + classes[index_max]
        color = (0, 0, 0)
        stroke = 1
        print(name)
        # web scrapping attempt
        WebScrp.set_name(classes[index_max].lower())
        rank, lp, account, message = WebScrp.pull_infomation()

        last_detected = datetime.now()

        while (datetime.now() - last_detected).total_seconds() < 2:

            cv2.putText(
                frame,
                "account: " + account,
                (200, 380),
                font,
                1,
                color,
                stroke,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame, "rank: " + rank, (200, 400), font, 1, color, stroke, cv2.LINE_AA
            )
            cv2.putText(
                frame, "lp: " + lp, (200, 430), font, 1, color, stroke, cv2.LINE_AA
            )
            cv2.putText(
                frame,
                "status: " + message,
                (200, 460),
                font,
                1,
                color,
                stroke,
                cv2.LINE_AA,
            )
            cv2.imshow("frame", frame)

            cv2.waitKey(1)
    # converting the frame to grey and looking for human faces
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.5, minNeighbors=5)

    # drawing a rectangle on detected human faces
    drawing_rectangles(grey, faces)

    # show the frame
    cv2.imshow("frame", frame)

    if cv2.waitKey(20) and 0xFF == ord("q"):
        break

# release the capture when everthing is done
cap.release()
cv2.destroyAllWindows()

from cProfile import label
import numpy as np
import cv2
from scipy.misc import face
import pickle

recongizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(
    'data\haarcascade_frontalface_alt.xml')

eye_cascade = cv2.CascadeClassifier(
    'data\haarcascade_eye.xml')
# reading the data
recongizer.read("trainner.yml")

# saving all the Label ID's to a dic
labels = {}
with open("labels.pickle", 'rb') as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}
    f.close()

cap = cv2.VideoCapture(0)

print(face_cascade)
while (True):
    # capture from by frame
    rect, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        grey, scaleFactor=1.5, minNeighbors=4)

    # print(faces)
    for (x, y, w, h) in faces:
        #print(x, y, w, h)

        # defining the ROI for the color and grey frame
        roi_grey = grey[y:y+h, x:x+w]
        roi_clor = frame[y:y+h, x:x+w]
        img_item = "img.png"
        cv2.imwrite(img_item, roi_grey)

        # drawing rectangle around the ROI
        color = (255, 0, 0)
        stroke = 2
        width = x+w
        height = y+h
        cv2.rectangle(frame, (x, y), (width, height), color, stroke)

        # finding eyes on the frame

        # getting the label and the confidence value
        id_, conf = recongizer.predict(roi_grey)

        if conf >= 60 and conf <= 99:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_PLAIN
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1,
                        color, stroke, cv2.LINE_AA)
    # show the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) and 0xFF == ord('q'):
        break

# release the capture when everthing is done
cap.release()
cv2.destroyAllWindows()

import os
from PIL import Image
import numpy as np
import cv2
import pickle


trained_face_data = cv2.CascadeClassifier(
    'data\haarcascade_frontalface_alt.xml')

# Getting the directory for the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# grabbing the directory of the faces folder
image_dir = os.path.join(BASE_DIR, "Faces")

recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0
label_ids = {}
x_train = []
y_labels = []

# see the files in the faces folder
for root, dirs, files in os.walk(image_dir):

    for file in files:
        # looking for files that end with png and jpg
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root, file)
            print(path)

            # creating a label for the images
            label = os.path.basename(os.path.dirname(
                path)).replace(" ", "-").lower()
            #print(label, path)

            # adding new images to the dictionary and adding a id to them
            if not label in label_ids:

                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]
            print(label_ids)

            pil_image = Image.open(path).convert(
                "L")  # turns images into grey scale
            size = (550, 500)

            finale_image = pil_image.resize(size, Image.ANTIALIAS)

            # adding the images into a SUPER array
            image_array = np.array(finale_image, "uint8")
            # print(image_array)
            faces = trained_face_data.detectMultiScale(
                image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
print(y_labels)
print(x_train)

# saving all the Label ID's
with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)
    f.close()
# using data to train the recognizer and saving its data
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")

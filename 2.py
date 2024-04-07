# It helps in identifying the faces
from datetime import datetime

import cv2, sys, numpy, os

from mdles.models import session, User, Dk

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

# Part 1: Create fisherRecognizer
print('Recognizing Face Please Be in sufficient Lights...')

# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1] < 80:
            print(names[prediction[0]])
            cv2.putText(im, '% s - %.0f' %
                        (names[prediction[0]], prediction[1]), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            try:
                facename = session.query(User).filter(User.ename == names[prediction[0]]).first()
                facename2 = session.query(Dk).filter(Dk.user_id == facename.id,
                                                     Dk.day == datetime.now().strftime("%Y-%m-%d")).first()
                print(facename2)
                if facename2 == None:
                    if datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") <= f"{datetime.now().strftime('%Y-%m-%d')}\t9:00:00":
                        print("上班成功", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              f"{datetime.now().strftime('%Y-%m-%d')} 9:00:00")
                        dk = Dk()
                        dk.zt = "上班正常"
                        dk.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        dk.user_id = facename.id
                        session.add(dk)
                        session.commit()
                        session.close()
                    else:
                        print("上班迟到")
                        dk = Dk()
                        dk.zt = "上班迟到"
                        dk.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        dk.user_id = facename.id
                        session.add(dk)
                        session.commit()
                        session.close()

                else:
                    if datetime.now().strftime("%Y-%m-%d %H:%M:%S") >= f"{datetime.now().strftime('%Y-%m-%d')} 17:50:08":
                        print("下班成功",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),f"{datetime.now().strftime('%Y-%m-%d')}\t17:50:08")
                        facename2.zt2="下班正常"
                        facename2.date2=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        session.commit()
                        session.close()

                    else:
                        print("早退")
            except:
                session.rollback()
            finally:
                session.close()

        else:
            cv2.putText(im, 'not recognized',
                        (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)

    if key == 27:
        break

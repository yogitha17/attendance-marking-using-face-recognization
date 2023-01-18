import cv2, numpy as np;
import xlwrite;
import time
import sys
from playsound import playsound

start = time.time()
period = 8
face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cas = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0);
recognizer = cv2.face.LBPHFaceRecognizer_create();
recognizer.read('trainer/trainer.yml');
flag = 0;
id = 0;
filename = 'filename';
data = {
    98: "P.Yogitha",
    84: "K.Lavanya",
    89: "L.Hyma",
    72: "G.Shireesha"

}
dict = {
    'item1': 1
}
# print(dict)
# font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 5, 1, 0, 1, 1)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, img = cap.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    faces = face_cas.detectMultiScale(gray, 1.3, 7);
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2);
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cas.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        id, conf = recognizer.predict(roi_gray)
        print("id  =  " + str(id))
        print("conf = " + str(conf))
        if (conf < 60):
             
            if id in data:
                 
                name = data[id]
                if (str(id)) not in dict:
                   
                    filename = xlwrite.output('attendance', 'class1', str(id), name, 'yes');
                    dict[str(id)] = str(id);
            else:
                id = 'Unknown, can not recognize'
                flag = flag + 1

        cv2.putText(img, str(id) + " " + str(conf), (x, y - 10), font, 0.55, (120, 255, 120), 1)
        # cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,(0,0,255));
    cv2.imshow('frame', img);
    # cv2.imshow('gray',gray);
    if flag == 100:
        playsound('transactionSound.mp3')
        print("Transaction Blocked")
        break;
    if time.time() > start + period:
        break;
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break;

cap.release();
cv2.destroyAllWindows();
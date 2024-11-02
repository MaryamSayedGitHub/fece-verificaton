
import cv2
import os
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db,storage


# إعداد Firebase Admin SDK
cred = credentials.Certificate('D:\\Face\\Faceverifdata.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceverifdata-default-rtdb.firebaseio.com/",
     'storageBucket': "faceverifdata.appspot.com"
})
bucket = storage.bucket()
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

# RealTime img

cap = cv2.VideoCapture(0)  
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  

    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame and encodeCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = [v * 4 for v in [y1, x2, y2, x1]] 
            
            # check if it matched or not 
            if matches[matchIndex]:
                
                id = studentIds[matchIndex]
                blob = bucket.get_blob(f'Images/{id}.jpg')
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                cv2.putText(img, "Verified", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                
                print( y1, x2, y2, x1 )
                cv2.line(img, (x1+10, y2-100), (x1+10,y1+120), (0, 225, 0), 3)
                cv2.line(img, (x1+10,y1+120 ), (x2,y2-100), (0, 225, 0), 3)
                

                # استرجاع بيانات الطالب من Firebase
                studentInfo = db.reference(f'Students/{id}').get()
                if studentInfo:
                  
                    name = studentInfo['name']
                    cv2.putText(img, f"Name: {name}", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  
                    cv2.putText(img, f"ID: {id}", (x1, y2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (2, 5, 0), 2)  # Integer thickness

            else:
                                
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 225), 3)
                cv2.line(img, (x1, y2), (x2, y1), (0,0, 225), 3)
                
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  
                cv2.putText(img, "Not Verified", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Webcam", img)

    # إغلاق الكاميرا عند الضغط على مفتاح المسافة
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

# تحرير وإغلاق الكاميرا تمامًا
cap.release()
cv2.destroyAllWindows()
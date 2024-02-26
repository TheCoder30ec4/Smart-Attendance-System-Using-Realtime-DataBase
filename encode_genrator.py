import cv2
import pickle
import face_recognition_models
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancesytem-858b1-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"attendancesytem-858b1.appspot.com"
})

folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    with open(fileName, "rb") as file:
        blob.upload_from_file(file)

def findEncodings(imagesList):
    encodingList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img)

        # Check if any face is detected in the image
        if len(face_locations) == 0:
            print("No face found in the image.")
            continue

        encode = face_recognition.face_encodings(img, face_locations)[0]
        encodingList.append(encode)
    return encodingList


print("started encoding.......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Completed encoding.!")

print("Creating a pickle file......")
file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("file saved")

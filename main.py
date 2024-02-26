import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancesytem-858b1-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"attendancesytem-858b1.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 751)
cap.set(4, 950)


imgBackground = cv2.imread('resources/Untitled.png')
window_width = 640
window_height = 480
# cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)  # Create a resizable window
# cv2.resizeWindow("Webcam", window_width, window_height)

def print_text(text:str, x,y):
    text = text
    position = (x,y)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 0, 0)  # BGR color (Blue, Green, Red)
    thickness = 5
    cv2.putText(imgBackground, text, position, font, font_scale, color, thickness)

print("Loding encoded file .... ")
file = open('EncodeFile.p','rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnowWithIds
print("Done loading.!")



counter = 0
id  =-1
imgStudent = []

while True:
    success, img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,faceCurFrame)





    webcam_frame_resized = cv2.resize(img, (window_width, window_height))
    start_y = 245  # Adjust this value to position the image lower
    start_x = 182  # Assuming you want to maintain the same horizontal position

    # Calculate the end coordinates
    end_y = start_y + img.shape[0]
    end_x = start_x + img.shape[1]
    #print(start_x,end_x)
    #print(start_y,end_y)

    # Now you can perform the assignment
    imgBackground[start_y:end_y, start_x:end_x] = webcam_frame_resized



    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print("matches", matches)
        #print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        #print("match Index", matchIndex)

        if matches[matchIndex]:
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            bbox = 182+x1,245+y1,x2-x1,y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                cvzone.putTextRect(imgBackground,"Loading",(500,500))
                counter  = 1

    if counter !=0:
        if counter ==1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            blob = bucket.get_blob(f'Images/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

            #update
            dateTimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                              "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - dateTimeObject).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 20:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                counter =0


        if 10<counter<20:
            img_resized = cv2.imread('resources/Untitled1.png', cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_resized, (202, 78))
            new_start_x = 964
            new_start_y = 570
            imgBackground[new_start_y:new_start_y + img_resized.shape[0],
            new_start_x:new_start_x + img_resized.shape[1]] = img_resized


        if counter<=10:
            print_text("name:", 150, 850)
            cv2.putText(imgBackground, str(studentInfo['name']), (250, 850), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 0), 2)
            print_text("Total_Attendance:", 150,900)
            cv2.putText(imgBackground, str(studentInfo['total_attendance']), (425, 900), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

            print_text("Position:", 150, 950)
            cv2.putText(imgBackground, str(studentInfo['Position']), (300, 950), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 0), 2)
            print_text("Year:", 600, 850)
            cv2.putText(imgBackground, str(studentInfo['Year']), (700, 850), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 0), 2)
            print_text("Id:", 600, 900)
            cv2.putText(imgBackground, str(studentInfo['Id']), (650, 900), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 0), 2)

        imgStudent_resized = cv2.resize(imgStudent, (209, 181))
        new_start_x = 964
        new_start_y = 350
        imgBackground[new_start_y:new_start_y+imgStudent_resized.shape[0], new_start_x:new_start_x+imgStudent_resized.shape[1]] = imgStudent_resized

        counter +=1

        if counter>=20:
            counter = 0
            studentInfo = []
            imgStudent=[]
            imgBackground[start_y:end_y, start_x:end_x] = webcam_frame_resized
            text_region_start = (100, 826)  # Top-left corner of the text region
            text_region_end = (850, 980)  # Bottom-right corner of the text region
            cv2.rectangle(imgBackground, text_region_start, text_region_end, (255, 255, 255), cv2.FILLED)
            img_resized = cv2.imread('resources/Untitled2.png', cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_resized, (202, 78))
            new_start_x = 964
            new_start_y = 570
            imgBackground[new_start_y:new_start_y + img_resized.shape[0],
            new_start_x:new_start_x + img_resized.shape[1]] = img_resized

    #cv2.imshow("Webcam",img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()

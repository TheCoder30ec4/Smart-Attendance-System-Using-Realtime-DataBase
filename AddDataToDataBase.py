import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancesytem-858b1-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')
data = {

    "0001":
        {
            "name":"Varun",
            "Year":"3rd",
            "Position": "Team lead",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0001"
        },
    "0002":
        {
            "name":"Tony",
            "Year":"4rd",
            "Position": "Vice captain",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0002"
        },
    "0003":
        {
            "name":"Thor",
            "Year":"4rd",
            "Position": "member",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0003"
        },
    "0004":
        {
            "name":"witch",
            "Year":"4rd",
            "Position": "Member",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0004"
        },
    "0005":
        {
            "name":"Hawkeye",
            "Year":"4rd",
            "Position": "Member",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0005"
        },
    "0006":
        {
            "name":"Bruce",
            "Year":"4rd",
            "Position": "Scientist",
            "total_attendance":3,
            "last_attendance_time":"2024-02-25 17:30:59",
            "Id":"0006"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
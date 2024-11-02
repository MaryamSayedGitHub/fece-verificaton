import firebase_admin
from firebase_admin import credentials, db

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('D:\Face\Faceverifdata.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceverifdata-default-rtdb.firebaseio.com/'
 })
ref = db.reference('Students')

data = {
    "2021170505":
    {
        "ID":2021170505,
        "name": "Elon Mask",
        "major": "Rocket Science",
        "starting_year": 2017, 
        "standing":"VG",
        "year": 3,
    },

     "2021170506":
    {
        "ID":2021170506,
        "name": "Jesse Cook",
        "major": "Music",
        "starting_year": 2020,
        "standing":"G",
        "year": 1,

    }
    
}

for key, value in data.items():
    ref.child(key).set(value)
    
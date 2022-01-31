import pyrebase

firebaseConfiguration = {
"apiKey": "AIzaSyAlzqAG9Ag670HIBzzjnIum6zpnk0o80t8",
  "authDomain": "ecommerce-flask.firebaseapp.com",
  "projectId": "ecommerce-flask",
  "storageBucket": "ecommerce-flask.appspot.com",
  "messagingSenderId": "180291136079",
  "appId": "1:180291136079:web:61b4affc41900d387c183a",
  "measurementId": "G-9C493M27G0"
}
firebase = pyrebase.initialize_app(firebaseConfiguration)
auth = firebase.auth()
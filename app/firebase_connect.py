import os
import firebase_admin
from firebase_admin import credentials, firestore

# Directly referencing firebase_key.json from the app directory
firebase_key_path = os.path.join(os.path.dirname(__file__), 'firebase_key.json')

if not os.path.exists(firebase_key_path):
    raise ValueError(f"The FIREBASE_KEY_PATH is not valid: {firebase_key_path}")

# Use the service account key to connect to Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def get_firestore_client():
    return db
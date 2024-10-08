import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv
load_dotenv()
firebase_key_contents = os.getenv('FIREBASE_KEY_CONTENTS')
if not firebase_key_contents:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not set.")
try:
    firebase_key_dict = json.loads(firebase_key_contents)
except json.JSONDecodeError as e:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not a valid JSON.") from e

cred = credentials.Certificate(firebase_key_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firestore_client():
    return db

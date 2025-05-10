import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase/firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_question(lecture_id, question_data):
    doc_ref = db.collection('lectures').document(lecture_id).collection('questions').document()
    doc_ref.set(question_data)

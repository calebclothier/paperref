"""Create a Firestore client for database CRUD operations"""

from firebase_admin import firestore


db = firestore.client()

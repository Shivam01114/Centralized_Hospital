from database.db import db
from datetime import datetime

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)   # ✅ ADD THIS

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    phone = db.Column(db.String(20))


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    disease = db.Column(db.String(50))
    result = db.Column(db.String(100))

    # ✅ ADD THIS
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
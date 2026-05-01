from flask import Blueprint, render_template, request, redirect, url_for, session
from database.models import Patient, Prediction
from database.db import db

main_bp = Blueprint('main', __name__)


# ================= HOME PAGE =================
@main_bp.route('/home')
def home():

    # ✅ LOGIN REQUIRED
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    return render_template('main/home.html')


# ================= SAVE PATIENT =================
@main_bp.route('/select', methods=['POST'])
def save_patient():
    try:
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('auth.login'))

        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")

        # ✅ validation
        if not name or not age:
            return "Name and Age are required"

        # ✅ find existing patient (1 user = 1 patient)
        patient = Patient.query.filter_by(user_id=user_id).first()

        if not patient:
            patient = Patient(
                user_id=user_id,
                name=name,
                age=int(age),
                gender=gender,
                phone=phone
            )
            db.session.add(patient)
        else:
            # ✅ update existing
            patient.name = name
            patient.age = int(age)
            patient.gender = gender
            patient.phone = phone

        db.session.commit()

        # ✅ store patient in session
        session['patient_id'] = patient.id

        return redirect(url_for('main.select_page'))

    except Exception as e:
        db.session.rollback()   # 🔥 IMPORTANT FIX
        return f"Error: {str(e)}"


# ================= DISEASE SELECT PAGE =================
@main_bp.route('/select', methods=['GET'])
def select_page():

    if not session.get('patient_id'):
        return redirect(url_for('main.home'))

    return render_template('main/select.html')


# ================= HISTORY =================
@main_bp.route('/history')
def history():

    patient_id = session.get('patient_id')

    if not patient_id:
        return redirect(url_for('main.home'))

    # ✅ handle created_at safely
    if hasattr(Prediction, "created_at"):
        data = Prediction.query.filter_by(
            patient_id=patient_id
        ).order_by(Prediction.created_at.desc()).all()
    else:
        data = Prediction.query.filter_by(
            patient_id=patient_id
        ).all()

    return render_template('main/history.html', data=data)
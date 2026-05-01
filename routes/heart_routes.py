from flask import Blueprint, render_template, request, send_file, session, redirect, url_for, jsonify
from services.heart_service import predict_heart
from database.models import Prediction
from database.db import db
import io

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    Spacer,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


heart_bp = Blueprint('heart', __name__)


# ================= HOME =================
@heart_bp.route('/heart')
def heart_home():
    if not session.get('patient_id'):
        return redirect(url_for('main.home'))

    return render_template('heart/overview.html')


# ================= PREDICT =================
@heart_bp.route('/heart/predict', methods=['POST'])
def heart_predict():
    try:
        patient_id = session.get('patient_id')

        if not patient_id:
            return redirect(url_for('main.home'))

        form = request.form

        # ✅ SAFE CONVERSION
        data = []
        for x in form.values():
            try:
                data.append(float(x))
            except:
                data.append(0)

        result = predict_heart(data)

        patient_data = {
            "Age": form.get("age"),
            "Chest Pain": form.get("cp"),
            "Resting BP": form.get("trestbps"),
            "Cholesterol": form.get("chol"),
            "Fasting Sugar": form.get("fbs"),
            "Rest ECG": form.get("restecg"),
            "Max Heart Rate": form.get("thalach"),
            "Exercise Angina": form.get("exang"),
            "Oldpeak": form.get("oldpeak"),
            "Slope": form.get("slope"),
            "CA": form.get("ca"),
            "Thal": form.get("thal"),
            "Result": "❤️ High Risk" if result == 1 else "✅ Low Risk",
            "Risk": "High" if result == 1 else "Low"
        }

        # ✅ session store
        session['last_patient_data'] = patient_data

        # ✅ DB save
        entry = Prediction(
            patient_id=patient_id,
            disease="Heart",
            result=patient_data["Result"]
        )

        db.session.add(entry)
        db.session.commit()

        return redirect(url_for('heart.heart_decision'))

    except Exception as e:
        return f"Error: {str(e)}"


# ================= DECISION PAGE =================
@heart_bp.route('/heart/decision')
def heart_decision():

    patient_data = session.get('last_patient_data')

    if not patient_data:
        return redirect(url_for('heart.heart_home'))

    return render_template('heart/decision.html', patient=patient_data)


# ================= REPORT PAGE =================
@heart_bp.route('/heart/reports')
def heart_reports():

    patient_data = session.get('last_patient_data')

    if not patient_data:
        return redirect(url_for('heart.heart_home'))

    return render_template('heart/reports.html', patient=patient_data)


# ================= DOWNLOAD PDF =================
@heart_bp.route('/heart/download_report', methods=['POST'])
def download_report():

    try:
        user = request.json or {}
        patient_data = session.get('last_patient_data')

        if not patient_data:
            return jsonify({"error": "No report available"}), 400

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        story = []

        # HEADER
        story.append(Paragraph("<b>🏥 CardioSense AI Hospital</b>", styles["Title"]))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        ))

        story.append(Spacer(1, 20))

        # PATIENT INFO
        story.append(Paragraph("<b>Patient Information</b>", styles["Heading2"]))

        for k, v in user.items():
            story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

        story.append(Spacer(1, 15))

        # RESULT
        story.append(Paragraph("<b>Diagnosis</b>", styles["Heading2"]))
        story.append(Paragraph(patient_data["Result"], styles["Normal"]))

        story.append(Spacer(1, 15))

        # PARAMETERS
        story.append(Paragraph("<b>Clinical Parameters</b>", styles["Heading2"]))

        for k, v in patient_data.items():
            story.append(Paragraph(f"{k}: {v}", styles["Normal"]))

        story.append(Spacer(1, 20))

        # RECOMMENDATION
        if "High" in patient_data["Risk"]:
            rec = "High risk detected. Consult doctor immediately."
        else:
            rec = "Low risk. Maintain healthy lifestyle."

        story.append(Paragraph("<b>Recommendation</b>", styles["Heading2"]))
        story.append(Paragraph(rec, styles["Normal"]))

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="Heart_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
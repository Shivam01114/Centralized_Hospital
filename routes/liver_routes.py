from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, send_file
from services.liver_service import predict_liver
from database.models import Prediction
from database.db import db
import io

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


liver_bp = Blueprint('liver', __name__)


# ================= HOME =================
@liver_bp.route('/liver')
def liver_home():
    if not session.get('patient_id'):
        return redirect(url_for('main.home'))

    return render_template('liver/index.html')


# ================= REPORT PAGE =================
@liver_bp.route('/liver/report')
def liver_report():
    if not session.get('liver_data'):
        return redirect(url_for('liver.liver_home'))

    return render_template('liver/report.html')


# ================= ABOUT =================
@liver_bp.route('/liver/about')
def liver_about():
    return render_template('liver/about.html')


# ================= CONTACT =================
@liver_bp.route('/liver/contact')
def liver_contact():
    return render_template('liver/contact.html')


# ================= PREDICT =================
@liver_bp.route('/liver/predict', methods=['POST'])
def liver_predict():
    try:
        patient_id = session.get('patient_id')

        if not patient_id:
            return jsonify({"error": "Session expired"}), 401

        form = request.form

        # ✅ input mapping
        data = [
            float(form.get("age")),
            float(form.get("gender")),
            float(form.get("tb")),
            float(form.get("db")),
            float(form.get("alk")),
            float(form.get("alt")),
            float(form.get("ast")),
            float(form.get("tp")),
            float(form.get("albumin")),
            float(form.get("agr"))
        ]

        result, risk = predict_liver(data)

        patient_data = {
            "Total Bilirubin": form.get("tb"),
            "Direct Bilirubin": form.get("db"),
            "Alkaline Phosphotase": form.get("alk"),
            "ALT": form.get("alt"),
            "AST": form.get("ast"),
            "Total Proteins": form.get("tp"),
            "Albumin": form.get("albumin"),
            "A/G Ratio": form.get("agr"),
            "Result": "⚠ High Risk" if result == 1 else "✅ Low Risk",
            "Risk": float(risk)
        }

        # ✅ session store
        session['liver_data'] = patient_data

        # ✅ DB save
        entry = Prediction(
            patient_id=patient_id,
            disease="Liver",
            result=patient_data["Result"]
        )

        db.session.add(entry)
        db.session.commit()

        return jsonify({
            "risk": float(risk),
            "result": patient_data["Result"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= DOWNLOAD PDF =================
@liver_bp.route('/liver/download_report', methods=['POST'])
def download_liver_report():

    try:
        patient_data = session.get('liver_data')

        if not patient_data:
            return jsonify({"error": "No report found"}), 400

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        story = []

        # ===== TITLE =====
        story.append(Paragraph("<b>🧪 Liver AI Medical Report</b>", styles["Title"]))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        ))

        story.append(Spacer(1, 20))

        # ===== PARAMETERS =====
        story.append(Paragraph("<b>Clinical Data</b>", styles["Heading2"]))

        for key, value in patient_data.items():
            story.append(Paragraph(f"{key}: {value}", styles["Normal"]))

        story.append(Spacer(1, 20))

        # ===== RESULT =====
        story.append(Paragraph("<b>AI Diagnosis</b>", styles["Heading2"]))
        story.append(Paragraph(patient_data["Result"], styles["Normal"]))

        story.append(Spacer(1, 20))

        # ===== RECOMMENDATIONS =====
        if "High" in patient_data["Result"]:
            recommendation = """
            • Avoid alcohol completely<br/>
            • Reduce oily food<br/>
            • Drink more water<br/>
            • Regular liver test<br/>
            • Consult doctor
            """
        else:
            recommendation = """
            • Maintain healthy diet<br/>
            • Regular exercise<br/>
            • Stay hydrated
            """

        story.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))
        story.append(Paragraph(recommendation, styles["Normal"]))

        story.append(Spacer(1, 20))

        story.append(Paragraph(
            "<i>This report is AI-generated. Consult doctor.</i>",
            styles["Italic"]
        ))

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="Liver_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
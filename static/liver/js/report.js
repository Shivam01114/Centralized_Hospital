// =====================================
// यकृत्‌दृष्टि – REPORT LOGIC
// ULTRA FULL VERSION (NO TRIM)
// DOCTOR AI + MULTI PAGE PDF + BG + SAFE MODE
// =====================================


// ======================================================
// 🔹 LOAD REPORT DATA
// ======================================================
const storedMedical = localStorage.getItem("reportData");

if (!storedMedical) {
    alert("Please analyze report first.");
    window.location.href = "/liver";   // ✅ FIX
}

const reportData = JSON.parse(storedMedical);


// ======================================================
// 🔹 SAFE PATIENT FALLBACK (IMPORTANT)
// ======================================================
const storedPatientInfo = JSON.parse(localStorage.getItem("patientInfo")) || {};

const patient = reportData.patient || {
    name: storedPatientInfo.name || "Patient",
    age: storedPatientInfo.age || "--",
    gender: storedPatientInfo.gender || "--"
};


// ======================================================
// 🔹 PAGE LOAD
// ======================================================
window.onload = () => {
    loadReport();
};


// ======================================================
// 🔹 RISK BASED DIET
// ======================================================
function getDietAdvice(risk) {

    if (risk < 40) {
        return "Balanced diet with fruits, vegetables, pulses, dairy and hydration.";
    }
    else if (risk < 60) {
        return "Low fat diet, avoid junk food, increase fiber and hydration.";
    }
    else {
        return "Strict diet control, avoid alcohol, processed food and oily items.";
    }
}


// ======================================================
// 🔹 WORKOUT
// ======================================================
function getWorkoutAdvice(risk) {

    if (risk < 40) {
        return "Daily walking, yoga and stretching.";
    }
    else if (risk < 60) {
        return "Moderate activity, avoid stress.";
    }
    else {
        return "Light activity only, avoid heavy workouts.";
    }
}


// ======================================================
// 🔹 LOAD REPORT UI
// ======================================================
function loadReport() {

    document.getElementById("patientName").innerText = patient.name;
    document.getElementById("patientAge").innerText = patient.age;
    document.getElementById("patientGender").innerText = patient.gender;

    document.getElementById("reportDiagnosis").innerText = reportData.diagnosis;
    document.getElementById("reportRisk").innerText = reportData.risk + "%";

    const list = document.getElementById("parameterList");
    list.innerHTML = "";

    Object.entries(reportData.parameters).forEach(([key, value]) => {

        const li = document.createElement("li");
        li.innerHTML = `<strong>${key}:</strong> ${value}`;
        list.appendChild(li);

    });

    reportData.diet = getDietAdvice(reportData.risk);
    reportData.workout = getWorkoutAdvice(reportData.risk);

    document.getElementById("dietPlan").innerText = "🥗 " + reportData.diet;
    document.getElementById("workoutPlan").innerText = "🏃 " + reportData.workout;
}


// ======================================================
// 🔊 AI DOCTOR VOICE (FULL DETAIL)
// ======================================================
function playVoiceReport() {

    const lang = document.getElementById("voiceLang").value;
    const risk = reportData.risk;

    let riskExplanation = "";

    if (risk < 40) {
        riskExplanation = "Low risk and normal liver function.";
    }
    else if (risk < 60) {
        riskExplanation = "Moderate liver risk detected.";
    }
    else {
        riskExplanation = "High risk of liver disease.";
    }

    let paramSpeech = "";
    for (let key in reportData.parameters) {
        paramSpeech += `${key} is ${reportData.parameters[key]}. `;
    }

    let message = "";

    if (lang === "en") {

        message = `
Hello ${patient.name}.
You are ${patient.age} years old.

Your liver risk score is ${risk} percent.
${riskExplanation}

Parameters:
${paramSpeech}

Diet:
${reportData.diet}

Workout:
${reportData.workout}

Consult doctor for confirmation.
        `;
    }
    else {

        message = `
नमस्ते ${patient.name}।
आपकी आयु ${patient.age} वर्ष है।

आपका जोखिम स्कोर ${risk} प्रतिशत है।
${riskExplanation}

पैरामीटर:
${paramSpeech}

आहार:
${reportData.diet}

व्यायाम:
${reportData.workout}
        `;
    }

    const speech = new SpeechSynthesisUtterance(message);
    speech.lang = lang === "hi" ? "hi-IN" : "en-IN";
    speech.rate = 0.9;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
}


// ======================================================
// 📄 ULTRA PROFESSIONAL PDF ENGINE (MULTI PAGE)
// ======================================================
async function generatePDF() {

    const jsPDF = window.jspdf?.jsPDF;
    if (!jsPDF) {
        alert("PDF engine missing");
        return;
    }

    const doc = new jsPDF("p", "mm", "a4");

    const PAGE_W = 210;
    const PAGE_H = 297;
    const M = 15;

    let y = 18;

    // ---------- TITLE ----------
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text("YAKRIT DRISHTI AI REPORT", PAGE_W / 2, y, { align: "center" });

    y += 8;

    doc.setFontSize(10);
    doc.text(`Generated: ${new Date().toLocaleString()}`, PAGE_W - M, y, { align: "right" });

    y += 12;

    // ---------- PATIENT ----------
    doc.setFontSize(12);
    doc.text(`Name: ${patient.name}`, M, y);
    doc.text(`Age: ${patient.age}`, 100, y);
    doc.text(`Gender: ${patient.gender}`, 150, y);

    y += 15;

    // ---------- DIAGNOSIS ----------
    doc.setFontSize(14);
    doc.text("Diagnosis", M, y);

    y += 8;

    doc.setFontSize(11);
    doc.text(reportData.diagnosis, M, y, { maxWidth: 180 });

    y += 10;
    doc.text(`Risk Score: ${reportData.risk}%`, M, y);

    y += 15;

    // ---------- PARAMETERS ----------
    doc.setFontSize(13);
    doc.text("Clinical Parameters", M, y);

    y += 8;

    doc.setFontSize(11);

    Object.entries(reportData.parameters).forEach(([k, v]) => {

        doc.text(`${k}: ${v}`, M, y);
        y += 6;

        if (y > 270) {
            doc.addPage();
            y = 20;
        }
    });

    y += 10;

    // ---------- DIET ----------
    doc.setFontSize(13);
    doc.text("Diet Recommendation", M, y);

    y += 8;

    doc.setFontSize(11);
    doc.text(reportData.diet, M, y, { maxWidth: 180 });

    y += 20;

    // ---------- WORKOUT ----------
    doc.setFontSize(13);
    doc.text("Workout Recommendation", M, y);

    y += 8;

    doc.text(reportData.workout, M, y, { maxWidth: 180 });

    y += 25;

    // ---------- DISCLAIMER ----------
    doc.setFontSize(10);
    doc.text(
        "AI generated report. Not a substitute for medical advice.",
        M,
        y,
        { maxWidth: 180 }
    );

    doc.save(`Liver_Report_${patient.name}.pdf`);
}
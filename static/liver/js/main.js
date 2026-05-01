// =====================================
// यकृत्‌दृष्टि – Predict Page JavaScript
// CENTRALIZED + FULL VERSION (FIXED)
// =====================================

// ---------- ELEMENTS ----------
const form = document.getElementById("predictForm");
const popup = document.getElementById("resultPopup");
const popupTitle = document.getElementById("popupTitle");
const popupMessage = document.getElementById("popupMessage");
const predictBtn = document.querySelector(".analyze-btn");
const patientModal = document.getElementById("patientModal");

const riskValueEl = document.getElementById("riskValue");
const gaugeFillEl = document.getElementById("gaugeFill");

// ---------- FORCE RESET ----------
if (!localStorage.getItem("patientInfo")) {
    sessionStorage.clear();
}

// ---------- PAGE LOAD ----------
window.onload = function () {

    if (patientModal) {
        patientModal.style.display = "flex";
    }

    if (form) {
        form.style.opacity = "0.3";
        form.style.pointerEvents = "none";
    }
};

// ---------- SAVE PATIENT ----------
function savePatient() {

    const name = document.getElementById("pname").value.trim();
    const age = document.getElementById("page").value.trim();
    const gender = document.getElementById("pgender").value;

    if (!name || !age || !gender) {
        alert("Please fill all patient details");
        return;
    }

    const patientData = {
        name: name,
        age: age,
        gender: gender
    };

    localStorage.setItem("patientInfo", JSON.stringify(patientData));

    sessionStorage.setItem("patientName", name);
    sessionStorage.setItem("patientAge", age);
    sessionStorage.setItem("patientGender", gender);

    document.getElementById("patientModal").style.display = "none";

    form.style.opacity = "1";
    form.style.pointerEvents = "auto";
}

// ---------- AI VOICE ----------
function speak(text) {
    if (!window.speechSynthesis) return;

    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = "en-IN";
    msg.rate = 0.95;

    speechSynthesis.cancel();
    speechSynthesis.speak(msg);
}

// ---------- FORM SUBMIT ----------
if (form) {
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        runPrediction();
    });
}

// ---------- RUN PREDICTION ----------
function runPrediction() {

    predictBtn.innerText = "Analyzing...";
    predictBtn.disabled = true;

    const formData = new FormData(form);

    // 🔥 FIXED ROUTE
    fetch("/liver/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        saveReportData(data);
        showPopup(data);

    })
    .catch(() => {
        alert("Prediction failed. Try again.");
    })
    .finally(() => {
        predictBtn.innerText = "Analyze Report";
        predictBtn.disabled = false;
    });
}

// ---------- SAVE REPORT DATA ----------
function saveReportData(data) {

    const risk = data.risk;

    const storedPatient =
        JSON.parse(localStorage.getItem("patientInfo")) || {};

    const diagnosisText =
        risk < 40
            ? "Low Risk – Clinically Normal"
            : risk < 60
                ? "Moderate Risk – Medical Attention Suggested"
                : "High Risk – Liver Disease Detected";

    const reportData = {
        patient: {
            name: sessionStorage.getItem("patientName") || storedPatient.name || "Patient",
            age: sessionStorage.getItem("patientAge") || storedPatient.age || "--",
            gender: sessionStorage.getItem("patientGender") || storedPatient.gender || "--"
        },
        diagnosis: diagnosisText,
        risk: risk,
        parameters: {
            "Total Bilirubin": form.tb.value,
            "Direct Bilirubin": form.db.value,
            "Alkaline Phosphotase": form.alk.value,
            "ALT": form.alt.value,
            "AST": form.ast.value,
            "Total Proteins": form.tp.value,
            "Albumin": form.albumin.value,
            "A/G Ratio": form.agr.value
        }
    };

    localStorage.setItem("reportData", JSON.stringify(reportData));
}

// ---------- SHOW POPUP ----------
function showPopup(data) {

    if (patientModal) {
        patientModal.style.display = "none";
    }

    popup.classList.remove("hidden");
    popup.classList.add("active");
    popup.style.display = "flex";

    const risk = Number(data.risk || 50);
    const name = sessionStorage.getItem("patientName") || "Patient";
    const age = sessionStorage.getItem("patientAge") || "--";

    riskValueEl.innerText = risk + "%";
    gaugeFillEl.style.width = risk + "%";

    popup.classList.remove("danger", "moderate");

    if (risk < 40) {
        popupTitle.innerText = "✅ Low Risk – Clinically Normal";
        popupMessage.innerText =
            `Patient ${name} (Age ${age}) shows normal liver health.`;
    }
    else if (risk < 60) {
        popup.classList.add("moderate");
        popupTitle.innerText = "⚠ Moderate Liver Risk";
        popupMessage.innerText =
            `Patient ${name} has moderate liver risk. Medical attention advised.`;
    }
    else {
        popup.classList.add("danger");
        popupTitle.innerText = "⚠ High Risk of Liver Disease";
        popupMessage.innerText =
            `Patient ${name} shows high risk of liver disease. Immediate consultation advised.`;
    }

    // 🔊 AI voice
    speak(popupTitle.innerText);
}

// ---------- CLOSE POPUP ----------
function closePopup() {

    popup.classList.remove("active");
    popup.classList.add("hidden");
    popup.style.display = "none";
}

// ---------- GO TO REPORT ----------
function goToReport() {
    window.location.href = "/liver/report";
}

// ---------- DEMO ----------
function demoDisease() {
    fillForm(60, 1, 8.5, 4.2, 320, 95, 110, 6.5, 2.8, 0.6);
}

function demoSafe() {
    fillForm(30, 0, 0.7, 0.2, 180, 22, 25, 7.4, 4.2, 1.2);
}

// ---------- FILL FORM ----------
function fillForm(age, g, tb, db, alk, alt, ast, tp, alb, agr) {

    form.age.value = age;
    form.gender.value = g;
    form.tb.value = tb;
    form.db.value = db;
    form.alk.value = alk;
    form.alt.value = alt;
    form.ast.value = ast;
    form.tp.value = tp;
    form.albumin.value = alb;
    form.agr.value = agr;
}

// ---------- CLEAR ----------
function clearForm() {
    form.reset();
    popup.classList.add("hidden");
}
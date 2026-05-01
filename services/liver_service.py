import os
import pickle
import numpy as np

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "rf_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")


# ================= LOAD MODEL =================
def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    with open(path, "rb") as f:
        return pickle.load(f)


# ================= INIT =================
try:
    model = load_model(MODEL_PATH)
    scaler = load_model(SCALER_PATH)

except Exception as e:
    print("❌ MODEL LOAD ERROR:", e)
    model = None
    scaler = None


# ================= PREDICT =================
def predict_liver(data):

    if model is None or scaler is None:
        raise Exception("Model or Scaler not loaded properly")

    try:
        # ✅ convert to numpy
        data = np.array(data, dtype=float).reshape(1, -1)

        # ✅ scale
        data = scaler.transform(data)

        # ✅ prediction
        prediction = int(model.predict(data)[0])
        prob = float(model.predict_proba(data)[0][1])

        return prediction, round(prob * 100, 2)

    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")
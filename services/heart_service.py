import joblib
import numpy as np

model = joblib.load("models/heart.pkl")

def predict_heart(data):
    data = np.array(data).reshape(1, -1)
    result = model.predict(data)
    return int(result[0])
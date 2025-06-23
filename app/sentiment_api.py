from flask import Flask, request, jsonify
import numpy as np
import pickle
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Modell és tokenizer betöltése
with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

model = load_model("models/sentiment_model.h5")

# Inference
def predict_sentiment(text):
    encoded = tokenizer.texts_to_matrix([text], mode='binary')
    pred = model.predict(np.array(encoded))
    label = np.argmax(pred)

    if label == 0:
        return "NEGATÍV"
    elif label == 1:
        return "SEMLEGES"
    else:
        return "POZITÍV"

@app.route('/')
def ping():
    return jsonify({"status": "API működik"}), 200

@app.route('/sentiment', methods=['POST'])
def sentiment():
    text = request.get_data(as_text=True)
    result = predict_sentiment(text)
    return jsonify({"sentiment": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

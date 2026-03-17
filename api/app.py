from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('Model/crop_model.pkl', 'rb'))

@app.route('/')
def home():
    return "Crop Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = [
            data['N'],
            data['P'],
            data['K'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall']
        ]
        input_array = np.array([features])
        prediction = model.predict(input_array)
        return jsonify({'crop': str(prediction[0]), 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})

if __name__ == '__main__':
    app.run(debug=True)

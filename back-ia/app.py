from flask import Flask, jsonify, request
from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')

target_names = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x', 'sci.electronics']

# Carregando o modelo treinado
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/')
def home():
    return "Welcome to the Predicted Class!"

# Definindo rota para a API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    new_data_vectorized = vectorizer.transform([data])
    predicted_category = model.predict(new_data_vectorized)[0]
    predicted_category = target_names[predicted_category]

    response = {'predicted_category': predicted_category}
    return jsonify(response)
    
if __name__ == '__main__':
    app.run()


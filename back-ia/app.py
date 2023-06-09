from flask import Flask, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')

# Carregar o modelo treinado
with open('model (1).pkl', 'rb') as file:
    model = pickle.load(file)

# Carregar o objeto de vetorização
with open('vectorizer (3).pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Definir as categorias desejadas
categories = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware','comp.sys.mac.hardware']

# Carregar o conjunto de dados 20 Newsgroups completo
full_data = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

# Vetorizar os dados de texto usando o objeto de vetorização carregado
X_full = vectorizer.transform(full_data.data)

# Converter as categorias em rótulos numéricos
labels_full = full_data.target

# Função para calcular a precisão para cada categoria
def calculate_category_accuracy():
    category_accuracy = {}
    for category in categories:
        category_indices = np.where(labels_full == categories.index(category) - categories.index(categories[0]))[0]
        category_predictions = model.predict(X_full[category_indices])
        accuracy = accuracy_score(labels_full[category_indices], category_predictions)
        category_accuracy[category] = accuracy
    return category_accuracy

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']

    if not text:
        return jsonify({'error': 'Input is empty'})

    # Vetorizar o texto de entrada
    text_vectorized = vectorizer.transform([text])

    # Fazer a predição
    predicted_label = model.predict(text_vectorized)[0]
    
    if predicted_label < len(categories):
        predicted_category = categories[predicted_label]
        category_accuracy = calculate_category_accuracy()[predicted_category]
    else:
        predicted_category = 'Categoria Desconhecida'
        category_accuracy = None

    result = {
        'predicted_category': predicted_category,
        'category_accuracy': category_accuracy
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run()


import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

    const categoryExplanations = {
    'comp.graphics': 'Computação gráfica',
    'comp.os.ms-windows.misc': 'Sistema Operacional Windows',
    'comp.sys.ibm.pc.hardware': 'Hardware de PC IBM',
    'comp.sys.mac.hardware': 'Hardware de Macs'
  };

  const handleInputChange = (e) => {
    setText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!text) {
      setError('Por favor, insira um texto antes de enviar.');
      setPrediction(null);
      return;
    }

    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();
    if (response.ok) {
      setPrediction(data);
      setError('');
    } else {
      setPrediction();
      setError(data.error);
    }
  };

    return (
    <div className="container">
      <h1 className="title">Classificação de Texto - Tecnologia</h1>
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="text" className="label">
            Insira um texto:
          </label>
          <textarea
          value={text}
          onChange={handleInputChange}
          className="input"
          rows="4"
          cols="40"
        ></textarea>
        </div>
        <button type="submit" className="button">
          Enviar
        </button>
      </form>
      {error && (
        <div className="error">
          <h4 className="error-text">Error: {error}</h4>
        </div>
      )}
      {prediction && (
        <div className="result">
          <h4 className="result-text">Categoria: {prediction.predicted_category}</h4>
          <p className="result-text">Accuracy: {(prediction.category_accuracy * 100).toFixed(2)}%</p>
        </div> 
        )}
      <div className="legend">
      <h3>Legenda:</h3>
      <ul>
        {Object.entries(categoryExplanations).map(([category, explanation]) => (
          <li key={category}>
            <strong>{category}:</strong> {explanation}
          </li>
        ))}
      </ul>
    </div>
    </div>
  );
}

export default App;
import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data: text }),
    });
    const data = await response.json();
    setCategory(data.predicted_category);
  };

  return (
    <div className="container">
      <h1 className="title">Text Classification</h1>
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="text" className="label">
            Enter Text:
          </label>
          <input
            type="text"
            className="input"
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
        <button type="submit" className="button">
          Submit
        </button>
      </form>
      {category && (
        <div className="result">
          <h4 className="result-text">Category: {category}</h4>
        </div>
      )}
    </div>
  );
}

export default App;

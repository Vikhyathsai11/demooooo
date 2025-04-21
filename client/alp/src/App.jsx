import React from 'react';
import './App.css';

function handleLogin(event) {
  event.preventDefault();
  const username = event.target.username.value;
  const password = event.target.password.value;

  // Send the login data to the server
  fetch('http://localhost:3000/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Invalid username or password.');
      }
    })
    .then((data) => {
      alert(data.message); // Show the server's response message
    })
    .catch((error) => {
      alert(error.message); // Show an error message
    });
}

function App() {
  return (
    <div className="login-container">
      <h1>hello world</h1>
    </div>
  );
}

export default App;

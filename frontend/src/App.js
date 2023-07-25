import React, { useState } from 'react';
import axios from 'axios';
import config from './config';
import './App.css';

const App = () => {
  const [isLogin, setIsLogin] = useState(true); // Set initial mode to Login
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  const handleSignUp = async () => {
    try {
      const response = await axios.post(`${config.apiUrl}/signup`, {
        name,
        email,
        password,
      });
      console.log(response.data.message);
      // Display welcome message here or redirect to another page after successful sign-up.
    } catch (error) {
      console.error(error.message);
      // Handle error and display error message.
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${config.apiUrl}/login`, {
        username,
        password: loginPassword,
      });
      // Handle successful login, e.g., store session token in cookies and redirect to dashboard.
      console.log(response.data); // The response should contain the session token or user info.
    } catch (error) {
      // Handle login failure, e.g., show error message.
      console.error(error.message);
    }
  };

  const toggleMode = () => {
    setIsLogin((prev) => !prev); // Toggle between Login and Sign Up mode
  };

  return (
    <div className="app-container">
      <h1>JobSearch Dashboard</h1>

      {/* Sign Up or Login Form based on mode */}
      {isLogin ? (
        <div className="form-container">
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <div>
              <label>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field"
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                className="input-field"
              />
            </div>
            <button type="submit">Login</button>
          </form>
          <p>
            Don't have an account? <button onClick={toggleMode}>Register</button>
          </p>
        </div>
      ) : (
        <div className="form-container">
          <h2>Sign Up</h2>
          <div>
            <label>Name:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
            />
          </div>
          <button onClick={handleSignUp}>Sign Up</button>
          <p>
            Already have an account? <button onClick={toggleMode}>Login</button>
          </p>
        </div>
      )}
    </div>
  );
};

export default App;

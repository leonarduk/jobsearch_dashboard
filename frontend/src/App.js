import React, { useState } from 'react';
import axios from 'axios';
import config from './config';
import './App.css';

const App = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [loggedInUserName, setLoggedInUserName] = useState(''); // Add loggedInUserName state
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleSignUp = async () => {
    try {
      const response = await axios.post(`${config.apiUrl}/signup`, {
        name,
        email,
        password,
      });
      console.log(response.data);

      // Update the success message state
      setSuccessMessage(response.data.message);

      // Update loggedInUserName state with the user's name
      setName(response.data.user_name);
      setLoggedInUserName(response.data.user_name);
      setIsAuthenticated(true); // Add this line

      // Clear form fields
      setName('');
      setEmail('');
      setPassword('');
    } catch (error) {
      console.error(error.message);
      setSuccessMessage(''); // Clear the success message
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
        console.log(response.data);

        // Update the success message state with the login success message
        setSuccessMessage('Login successful');

        // Update loggedInUserName state with the user's name
        setName(response.data.user_name);
        setLoggedInUserName(response.data.user_name);
        setIsAuthenticated(true); // Add this line

        // Set the user name in the state
        setName(response.data.user_name);

        // Handle successful login here or redirect to dashboard.
      } catch (error) {
        console.error(error.message);

        // Update the success message state with the login error message
        setSuccessMessage('Login failed. Please check your username and password.');
      }
    };

    const handleLogout = () => {
      setIsAuthenticated(false);
      setLoggedInUserName('');
      setUsername('');
      setLoginPassword('');
      setSuccessMessage('Logged out successfully.');
    };

  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    setSuccessMessage(''); // Clear the success message
  };

return (
  <div className="app-container">
    <h1>JobSearch Dashboard</h1>

    {!isAuthenticated ? (
      isLogin ? (
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
      )
    ) : (
      <div>
        {/* Display the "Hello" message with the user's name */}
        {loggedInUserName && <p>Hello, {loggedInUserName}!</p>}

        {/* Display success message */}
        {successMessage && <p className="success-message">{successMessage}</p>}

        {/* Logout Button */}
        <button onClick={handleLogout}>Logout</button>
      </div>
    )}
  </div>
);

};

export default App;

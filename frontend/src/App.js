import React, { useState } from 'react';
import axios from 'axios';
import config from './config';
import './App.css';
import UserProfile from './UserProfile';

const LoginForm = ({ onLoginSuccess, toggleMode }) => {
  const [username, setUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    // API call logic for login
    try {
      const response = await axios.post(`${config.apiUrl}/login`, {
        username,
        password: loginPassword,
      });

      if (response.data && response.data.user_name) {
        onLoginSuccess(response.data.user_name);
      }
    } catch (error) {
      console.error(error.message);
      // Handle error scenarios here (e.g., show error message to user)
    }
  };

  return (
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
  );
};

const SignupForm = ({ onSignupSuccess, toggleMode }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = async () => {
    // API call logic for signup
    try {
      const response = await axios.post(`${config.apiUrl}/signup`, {
        name,
        email,
        password,
      });

      if (response.data && response.data.user_name) {
        onSignupSuccess(response.data.user_name);
      }
    } catch (error) {
      console.error(error.message);
      // Handle error scenarios here (e.g., show error message to user)
    }
  };

  return (
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
  );
};

const App = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false); // Add this for loading state
  const [loggedInUserName, setLoggedInUserName] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState(''); // Add this for error messages

  const handleLoginSuccess = (userName) => {
    setIsLoading(false);
    setLoggedInUserName(userName);
  };

  const handleSignupSuccess = (userName) => {
    setIsLoading(false);
    setLoggedInUserName(userName);
  };

  const handleLogout = () => {
    setLoggedInUserName('');
    setSuccessMessage('Logged out successfully.');
  };

  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    setSuccessMessage(''); // Clear the success message
    setErrorMessage(''); // Clear the error message
  };

  return (
    <div className="app-container">
      <h1>JobSearch Dashboard</h1>

      {isLoading ? (
        <p>Loading...</p>
      ) : !loggedInUserName ? (
        isLogin ? (
          <LoginForm onLoginSuccess={handleLoginSuccess} toggleMode={toggleMode} />
        ) : (
          <SignupForm onSignupSuccess={handleSignupSuccess} toggleMode={toggleMode} />
        )
      ) : (
        <UserProfile userName={loggedInUserName} onLogout={handleLogout} />
      )}

      {/* Display success and error messages */}
      {successMessage && <p className="success-message">{successMessage}</p>}
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
};

export default App;

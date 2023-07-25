// App.js
import React, { useState } from 'react';
import axios from 'axios';
import Login from './Login'; // Import the Login component

function App() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = async () => {
    // Your existing handleSignUp function for sign up
    try {
      const response = await axios.post(
        'http://localhost:4000/dev/signup',
        {
          name: name,
          email: email,
          password: password,
        }
      );
      console.log(response.data.message);
      // Display welcome message here or redirect to another page after successful sign-up.
    } catch (error) {
      console.error(error.message);
      // Handle error and display error message.
    }
  };

  return (
    <div>
      <h1>JobSearch Dashboard Sign Up</h1>
      <div>
        <label>Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <button onClick={handleSignUp}>Sign Up</button>

      {/* Render the Login component */}
      <Login />
    </div>
  );
}

export default App;

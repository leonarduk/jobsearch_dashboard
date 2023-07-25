import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = async () => {
      //'https://1bfjki6cdh.execute-api.eu-west-1.amazonaws.com/dev/signup',
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
//      console.error(error.response.data.message);
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
    </div>
  );
}

export default App;

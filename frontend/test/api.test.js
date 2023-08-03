// src/App.test.js

import React from 'react';
console.log(React)

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import App from '../src/App';

// Create a new instance of the axios mock adapter
const mockAxios = new MockAdapter(axios);

// Mock the responses for the API endpoints
mockAxios
  .onPost('http://localhost:4000/dev/signup', {
    name: 'Test User',
    email: 'test@example.com',
    password: 'password',
  })
  .reply(200, { message: 'User created successfully!' });

mockAxios
  .onPost('http://localhost:4000/dev/login', {
    username: 'testuser',
    password: 'password',
  })
  .reply(200, { token: 'fakeToken123' });

describe('App Integration Test', () => {
  it('should render the login form and handle login', async () => {
    // Render the App component
    render(<App />);

    // Expect login form elements to be present
    const loginForm = screen.getByText('Login');
    const usernameInput = screen.getByLabelText('Username:');
    const passwordInput = screen.getByLabelText('Password:');
    const loginButton = screen.getByText('Login');

    // Enter credentials and click the login button
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'password' } });
    fireEvent.click(loginButton);

    // Wait for the API call to finish
    await waitFor(() => {
      expect(screen.getByText('JobSearch Dashboard')).toBeInTheDocument();
      expect(screen.queryByText('Login')).toBeNull();
      expect(screen.getByText('User created successfully!')).toBeInTheDocument();
    });
  });

  it('should render the sign-up form and handle sign-up', async () => {
    // Render the App component
    render(<App />);

    // Expect sign-up form elements to be present
    const signUpButton = screen.getByText('Register');

    // Click the sign-up button to toggle mode
    fireEvent.click(signUpButton);

    // Expect sign-up form elements to be present after toggling mode
    const nameInput = screen.getByLabelText('Name:');
    const emailInput = screen.getByLabelText('Email:');
    const passwordInput = screen.getByLabelText('Password:');
    const signUpButtonAfterToggle = screen.getByText('Sign Up');

    // Enter sign-up credentials and click the sign-up button
    fireEvent.change(nameInput, { target: { value: 'Test User' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password' } });
    fireEvent.click(signUpButtonAfterToggle);

    // Wait for the API call to finish
    await waitFor(() => {
      expect(screen.getByText('JobSearch Dashboard')).toBeInTheDocument();
      expect(screen.queryByText('Sign Up')).toBeNull();
      expect(screen.getByText('User created successfully!')).toBeInTheDocument();
    });
  });
});

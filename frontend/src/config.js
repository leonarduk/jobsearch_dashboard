// config.js
const isLocal = window.location.hostname === 'localhost';

const config = {
  apiUrl: isLocal ? 'http://localhost:4000/dev' : 'https://1bfjki6cdh.execute-api.eu-west-1.amazonaws.com/dev/',
};

export default config;

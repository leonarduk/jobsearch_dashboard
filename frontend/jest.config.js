module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
     "^.+\\.js$": "babel-jest",
      "^.+\\.css$": "jest-css-modules-transform"

  },
//  preset: "@vue/cli-plugin-unit-jest",
  transformIgnorePatterns: [
      "node_modules/(?!axios)/",
      "/node_modules/",
      "\\.css$"
    ],

  moduleNameMapper: {
    '^axios$': require.resolve('axios'),
  "\\.(css)$": "identity-obj-proxy"
  },
  setupFilesAfterEnv: ['./test/setupTests.js']

};


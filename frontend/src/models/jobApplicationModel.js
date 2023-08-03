const mongoose = require('mongoose');

const jobApplicationSchema = new mongoose.Schema({
  // Define your schema fields here, for example:
  company: { type: String, required: true },
  position: { type: String, required: true },
  dateApplied: { type: Date, required: true },
  // Add other fields as needed
});

const JobApplication = mongoose.model('JobApplication', jobApplicationSchema);

module.exports = JobApplication;

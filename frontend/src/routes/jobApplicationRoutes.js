const express = require('express');
const jobApplicationController = require('../controllers/jobApplicationController');

const router = express.Router();

// Define the routes for the CRUD APIs
router.post('/api/jobApplications', jobApplicationController.createJobApplication);
router.get('/api/jobApplications/:id', jobApplicationController.readJobApplication);
router.put('/api/jobApplications/:id', jobApplicationController.updateJobApplication);
router.delete('/api/jobApplications/:id', jobApplicationController.deleteJobApplication);
router.get('/api/jobApplications', jobApplicationController.listJobApplications);

module.exports = router;

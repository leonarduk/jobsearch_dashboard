Running Locally

# run front end locally on http://localhost:3000

cd jobsearch_dashboard\frontend
npm start

# run lambda locally on http://localhost:4000

cd jobsearch_dashboard\jd_backend
serverless offline start

Deploying to AWS

# deploy lambda to AWS

cd jobsearch_dashboard\jd_backend
serverless deploy

# note

To enable CORS in Firefox, you can follow these steps:

    Open Firefox and go to about:config.
    In the search bar, type security.fileuri.strict_origin_policy.
    Double-click on the entry to change its value to false.
    Restart Firefox.

curl -m 610 -X POST https://us-central1-assignment-1-391514.cloudfunctions.net/baseball 
-H "Authorization: bearer $(gcloud auth print-identity-token)" 
-H "Content-Type: application/json" 
-d '{  "bucket": "3216984651",
        "path": "batch",
        "separateLines": "False",
        "start_date": "2023-01-01",
        "end_date": "2023-8-10" }'

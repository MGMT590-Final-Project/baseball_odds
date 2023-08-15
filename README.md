# baseball_odds
Repository to hold code related to Purdue MGMT-590 final project Summer 2023

This project aims to predict real-time winning odds for major league baseball games.  

We utilize Google Cloud Platform to accomplish this goal. We use several services in conjunction. We will break them into to parts.

Training
------------
1. Google Cloud Function (GCF)
2. Google Cloud Console (GCC)
3. Google Cloud Storage (GCS)
4. Google Big Query (GBQ)

Desc: Using GCF we set a function found in ./streaming/ to pull data as csv between dates and insert it into (GCS). We iteratively pull one year at a time by triggering GCF with GCC. Once this data is loaded into GBQ we run 

Streaming
------------
1. Google Cloud Function
2. Google Cloud Scheduler
3. Google Cloud Storage
4. Pub/Sub
6. Dataflow
7. Google Big Query
8. looker

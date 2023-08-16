# baseball_odds
Repository to hold code related to Purdue MGMT-590 final project Summer 2023

This project aims to predict real-time winning odds for major league baseball games.  

We utilize Google Cloud Platform to accomplish this goal. We use several services in conjunction. We will break them into two parts.

Training
------------
1. Google Cloud Function (GCF)
2. Google Cloud Console (GCC)
3. Google Cloud Storage (GCS)
4. Google Big Query (GBQ)

Desc:  
Using GCF, we set the function found in ./streaming/ to pull data as CSV between dates and insert it into (GCS). We iteratively pull one year at a time by triggering GCF with GCC. Once this data is loaded into GBQ, we run ./model/final_score.sql to create our training data.

Streaming
------------
1. Google Cloud Function
2. Google Cloud Scheduler
3. Google Cloud Storage
4. Pub/Sub
6. Dataflow
7. Google Big Query
8. looker

Desc: 
In this section, we create a live* streaming pipeline. We utilize the same GCF function found in  ./streaming/ to pull in data. this time, we pull the data in a row at a time as a JSON file. Once the data is available in GCS, we utilize a Dataflow pipe to move it to Pub/Sub. Pub/Sub handles any duplication of files. We then utilize Dataflow again to pipe the data into GBQ. This data is then available to be queried by Looker in our dashboard. 

*Note  
Streaming data is more challenging for this task. Because the data in Pybaseball is only available from the previous day, we must create delayed streaming. To do this, we only pull in data that is older than 24 hours.    

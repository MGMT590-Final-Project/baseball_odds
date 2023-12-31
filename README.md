# baseball_odds
#### Repository holds code related to Purdue MGMT-590 final project Summer 2023.

###### This project aims to predict real-time winning odds for major league baseball games.  

We utilize Google Cloud Platform to accomplish this goal. We use several services in conjunction. We will break them into two parts.

Training
------------
###### Services used:

1. Google Cloud Function (GCF)
2. Google Cloud Console (GCC)
3. Google Cloud Storage (GCS)
4. Google Big Query (GBQ)

###### Description:  
Using GCF, we set the function found in ./streaming/ to pull data as CSV between dates and insert it into (GCS). We iteratively pull one year at a time by triggering GCF with GCC. Once this data is loaded into GBQ, we run ./model/final_score.sql to create our training data's target. Once we had the training data we followed the procedure outlined in the notebook ./model/GameDataPrediction.ipynb.

Streaming
------------
###### Services used:

1. Google Cloud Function
2. Google Cloud Scheduler
3. Google Cloud Storage
4. Pub/Sub
6. Dataflow
7. Google Big Query
8. looker

###### Description:  
In this section, we create a live* streaming pipeline. We utilize the same GCF function found in  ./streaming/ to pull in data. this time, we pull the data in a row at a time as a JSON file. Once the data is available in GCS, we utilize a Dataflow pipe to move it to Pub/Sub. Pub/Sub handles any duplication of files. We then utilize Dataflow again to pipe the data into GBQ. This data is then available to be queried by Looker in our dashboard.

Introducing MLB Game Tracker: Revolutionizing Baseball Analysis in Real Time.  In the world of baseball, every pitch, swing, and play can shift the course of a game in seconds.  With MLB Game Tracker, we're taking baseball analysis to a whole new level by harnessing live game data to provide instant win probabilities.  Imagine having a real-time dashboard that not only captures the action on the field but also calculates the likelihood of victory based on historical data, player performance, and situational analysis.  
Whether you're a passionate fan following the game from the stands or a coach making critical decisions in the dugout, MLB Game Tracker empowers you with actionable insights.  Our advanced algorithms process data at lightning speed, allowing you to anticipate momentum shifts, identify strategic opportunities, and truly understand the dynamics of the game.  
But it's not just about the numbers!  MLB Game Tracker is a game-changer for everyone who lives and breathes baseball.  We're not just providing stats – we're creating an immersive experience that adds depth to your understanding of the game.  Join us on this journey to redefine how we interact with baseball, and be part of a community that values both the art and science of the sport.  
Step up to the plate with MLB Game Tracker and be at the forefront of the next generation of baseball analysis.  Elevate your passion for the game and experience the excitement of predicting victory like never before.  

###### *Note  
Acquiring streaming data is challenging for this task. Because the data in Pybaseball is only available from the previous day, and getting live data from MLB can require special permission, we must create delayed streaming. To do this, we only pull in data that is older than 24 hours.    

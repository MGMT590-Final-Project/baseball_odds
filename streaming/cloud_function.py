import json
import logging
import datetime
import argparse
import numpy as np
from google.cloud import storage
from pybaseball import statcast
import pandas as pd
import requests

logging.basicConfig(format='%(asctime)s.%(msecs)03dZ,%(pathname)s:%(lineno)d,%(levelname)s,%(module)s,%(funcName)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
_logger = logging.getLogger(__name__)

class Storage(object):
    _increment = 0

    def _createFileName(self):
        """
        CREATE FILE NAME TO PASS TO GCS

        Returns
        -------
        filename : STR
            FILE NAME IS DATE TIME AND SQUENTIAL ORDER.

        """
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_' + str(self._increment)
        self._increment += 1
        return filename

    def __init__(self, bucket, folder=None, separateLines=False, project=None, credentials=None):
        self._bucket = bucket
        self._client = storage.Client().bucket(self._bucket)
        self._path = ('baseballData' if folder is None else folder)
        self._separateLines = separateLines

    def process(self, data):
        """
        Process statcast data object.
        If getting streaming add a timestamp and post each line to gcs
        If archive data send as one csv

        Parameters
        ----------
        data : pd.dataframe
            DATASET THAT CONTAINS ALL OF YESTERDAYS BASEBALL DATA.

        """
        
        if self._separateLines == 'True':
            df_game_time = pd.DataFrame(columns = ['game_pk','at_bat_number','playEndTime'])

            # get play by play data from mlb. This has timestamps of plays
            for game in data.game_pk.unique():
                url = f"http://statsapi.mlb.com/api/v1/game/{game}/playByPlay"
                response = requests.get(url)
                time_data = response.json()['allPlays']
                
                #iterate over baseball plays and get timestamps
                for bat in time_data:
                    df_game_time = pd.concat([df_game_time,
                                            pd.DataFrame([[game,bat['atBatIndex']+1,time_data[bat['atBatIndex']]['playEndTime']]],
                                                        columns = ['game_pk','at_bat_number','playEndTime'])])
            
            #merge timestamps onto statcastdata
            df_w_ts = data.merge(df_game_time,how = 'left', on = ['game_pk','at_bat_number'])
            
            #get datetime from 24 hours ago
            ts_yesterday = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
            
            #filter out all data new than 24hrs old to dummy streaming data
            df_w_ts.loc[:,'game_date1'] = df_w_ts.loc[:,'game_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df_w_ts = df_w_ts.drop(columns=['game_date'])               
            df_w_ts = (df_w_ts
            .loc[df_w_ts.playEndTime
                .apply(lambda x: datetime.datetime
                        .strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')) <= ts_yesterday,:]
            .rename(columns={'fielder_2.1':'fielder_2_1','pitcher.1':'pitcher_1','game_date1':'game_date'})
            )
            
            #split the dataframe into rows and convert to json files for stream
            for n, group in df_w_ts.groupby(np.arange(len(df_w_ts))):
                fullpath = self._path + '/' + self._createFileName() + '.json'
                self._client.blob(fullpath).upload_from_string(group.to_json(orient='records',lines = True), 'text/json')
                
        #send as one csv
        else: 
            fullpath = self._path + '/' + self._createFileName() + '.csv'
            self._client.blob(fullpath).upload_from_string(data.to_csv(), 'text/csv')

def main(request, credentials=None):
    """
    Get parameters for cloud call
    use them to retrive data
    add data to google cloud storage.

    Parameters
    ----------
    request : parser.parse_args()
        OBJECT HOLDS PARAMETERS FOR FUNCTION.
    credentials : TYPE, optional
        DESCRIPTION. The default is None.
        
    """

    # pull parameters from cloud call
    messageJSON = json.loads(request.get_data(as_text=True))
    bucket = messageJSON.get('bucket', None)
    path = messageJSON.get('path', None)
    separateLines = messageJSON.get('separateLines', False)
    start_date = messageJSON.get('start_date', None)
    end_date = messageJSON.get('end_date', None)

    #get statcast data
    data = statcast(start_date, end_date)

    if bucket:
        # create instance of google cloud storage
        storage_instance = Storage(bucket, folder=path, separateLines=separateLines, credentials=credentials)

        #add data to google cloud storage
        storage_instance.process(data)

    pass

if __name__ == '__main__':
    
    # Read in parsed variables from cloud call
    parser = argparse.ArgumentParser(description="Fetch baseball data and save to GCS.")
    
    parser.add_argument('-separateLines', help='Store each record as a separate file in GCS.', action="store_true", default=False)
    parser.add_argument('-bucket', help='GCS bucket name to save the data.', required=True)
    parser.add_argument('-path', help='Path within the GCS bucket to save the data.', default=None)
    parser.add_argument('-start_date', help='Start date to fetch baseball data (format: YYYY-MM-DD).', required=False)
    parser.add_argument('-end_date', help='End date to fetch baseball data (format: YYYY-MM-DD).', required=False)
    
    args = parser.parse_args()

    #example of data request
        #request_data = {
        #    "bucket": "3216984651",
        #    "path": "live",
        #    "separateLines": False,
        #    "start_date": "2023-07-01",
        #    "end_date": "2023-07-02"
        #}
    
    main(args())

########################################################################
########################################################################
# This script is for those who have used 'Backupery for Slack Workspace' 
# to download their Slack workspace data. Backupery saves each workspace
# as a folder with that channel's name, and each folder will contain
# a .json file for each day's messages for the duration of the 
# channel's lifespan. This script loops through all of the .json 
# files in a given Slack workspace folder, and combines all of the 
# messages into a single .csv file for easier reference.
#
# Currently, this script only saves user, text, timestamp, and team
# values, but this could be expanded to include reactions, links, etc.
########################################################################
########################################################################

import os, json
import pandas as pd
from datetime import datetime

# Change to your Slack messages channel folder (general, random, etc.) 
directoryString = '/PATH/TO/YOUR/FOLDER'
directory = os.chdir(directoryString)

# Create Pandas DataFrame
cols = ['user', 'text', 'timestamp', 'team']
messages = pd.DataFrame(columns=cols)

# Loop through .json files in folder
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(directoryString + "/" + filename) as data_file:
            data = json.load(data_file)
            for message in data:
                user = message['user'] if 'user' in message else 'unknown'
                text = message['text'] if 'text' in message else 'unknown'
                timestamp = datetime.fromtimestamp(float(message['ts'])) if 'ts' in message else 'unknown'
                team = message['team'] if 'team' in message else 'unknown'

                messages = messages.append({'user': user, 'text': text, 'timestamp': timestamp, 'team': team}, ignore_index=True)
    else:
        continue

# Create 'channel_messages.csv'
messages.to_csv('channel_messages', sep='\t', encoding='utf-8', index=False)
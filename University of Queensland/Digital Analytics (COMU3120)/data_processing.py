import time
import json
import requests

token = 'BQARki_ztRsCcA0lPrFPEB2seGA_JXucVvv1dz4hzJt-elLIOrZgqHNegcYFSLzexSUUJxrNyq74Uybg99uflbTGXOLRSAlVTGtYuQh4p3j7BYxcQP7buOxWiJI_Ew_-GPnkDZHDsgjGHfvPpXPSIvd-Dj1bais2b3gU1Ea8j2sgoH_Xh_k'

headers ={
    'Accept':'application/json',     
    'Content-Type':'application/json',
    'Authorization':'Bearer ' + token,
}

feature_list = open('features.csv')
final_id = ''

for line in feature_list:
    meta = line.split(',')
    final_id = meta[11].replace('\n','')


feature_list.close()

track_list = open('tracks.csv')
feature_list = open('features.csv', 'a')
counter = 0
stat = dict()
stat['count'] = 0
useless_field = ['uri', 'track_href', 'analysis_url', 'type', 'duration_ms', 'time_signature']
start = False

for line in track_list:
    
    meta = line.split(',')
    year = meta[0]
    artist = meta[1]
    track = meta[2]
    track_id = meta[3].replace('\n', '')

    if final_id == '': start = True

    if track_id == final_id: start = True
    
    if start is False: continue

    
    response = requests.get('https://api.spotify.com/v1/audio-features/' + track_id, headers=headers)
    print(response.text)
    write_line = ''
    if len(response.text) > 100:
        data = json.loads(response.text)
        for key in data:
            if key not in useless_field:
                write_line += str(data[key])
                write_line += ','
    if track_id != final_id and write_line != '':
        feature_list.write(write_line[0: -1] + '\n')
    time.sleep(1)

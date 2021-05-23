import pandas as pd
import requests
import json
import time

token = 'BQBXq32jpkXrDO65sYa7ss1lZ1X9Ehc0h4EMDP-HmTYPDAO6x1IZfGFeNAlfNnr0tVmrYfPkdEzCEKMvhokU4b6v7tCDaMtw10hK9YjaWlRK3MozAyM_lT4hKoWEXET_43OGjYFnyDWQ6YpD7ryA5TK8v6KI2cTJJ9sUvvPm_wilD0ShOEY'

headers ={
    'Accept':'application/json',     
    'Content-Type':'application/json',
    'Authorization':'Bearer ' + token,
}

track_list = open('tracks.csv')
final_artist = ''
final_track = ''
final_year = ''

for line in track_list:
    meta = line.split(',')
    final_year = meta[0]
    final_artist = meta[1]
    final_track = meta[2]

track_list.close()

music_list = open('chartdata.csv')
track_list = open('tracks.csv', 'a')

start = False

for line in music_list:
    
    meta = line.split(';')
    year = meta[0]
    artist = meta[1]
    track = meta[2].replace('\n', '')

    if artist == final_artist and track == final_track and year == final_year:
        start = True

    if start is False:
        continue

    print(artist, track)

    params = (
        ('q', artist + ' ' + track),
        ('type', 'track'),
        ('limit', '1')
    )

    if not (artist == final_artist and track == final_track and year == final_year):
        response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        data = json.loads(response.text)
        #print(data)
        if 'tracks' in data and 'items' in data['tracks']:
            if len(data['tracks']['items']) > 0:
                if 'id' in data['tracks']['items'][0]:
                    id = data['tracks']['items'][0]['id']
                    track_list.write(year + ',' + artist + ',' + track + ',' + id + '\n')
                    print(id)
                    time.sleep(1)
            
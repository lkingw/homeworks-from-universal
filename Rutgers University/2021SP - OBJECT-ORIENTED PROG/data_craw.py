import requests

import json
import time

url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# the GET request parameters
params = {
        'api-key': 'GASyPHXJQMTYu5VVD5uNbeCmGQ7EwFyD',
        'q': 'covid-19',
        'begin_date': '20191201',
        'end_date': '20191209',
        'sort': 'newest'
    }

# to store the data
results = []

# request data via NYTimes' API with different page number

for i in range(0, 100):

    # sleep a little time to aviod API baning
    time.sleep(5)
    params['page'] = i
    response = requests.get(url, params = params)
    data = response.json()
    responses = data['response']['docs']
    print('page ' + str(i))

    # extract the required data
    for response in responses:
        
        meta = {}
        main = response['headline']['main']
        keywords = response['keywords']
        date = response['pub_date']
        words = []
        for word in keywords:
            words.append(word['value'])
        abstract = response['abstract']
        
        meta['core'] = main
        meta['keywords'] = words
        meta['abstract'] = abstract
        meta['date'] = date
        results.append(meta)

# store data as a JSON file
text = json.dumps(results, sort_keys=True, indent=4)
sample = open('data_slice_14_0_100.json', 'w')
sample.write(text)
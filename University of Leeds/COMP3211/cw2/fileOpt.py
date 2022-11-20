import json

countryDatasetPath = './static/country.json'
countryData = dict()

try:
    filehandle = open(countryDatasetPath, 'r')
    countryData = json.load(filehandle)
finally:
    filehandle.close()

def getDatabase():
    return countryData
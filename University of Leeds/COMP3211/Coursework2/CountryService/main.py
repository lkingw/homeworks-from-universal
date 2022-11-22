from flask_restful import Resource, Api
from flask import Flask
from math import sin, cos, radians, acos
import json

countryDatasetPath = './CountryService/country.json'
filehandle = open(countryDatasetPath, 'r')
countryData = json.load(filehandle)

def getGeoDistance(lat1, lon1, lat2, lon2, r=6371):
    coordinates = lat1, lon1, lat2, lon2
    phi1, lambda1, phi2, lambda2 = [
        radians(c) for c in coordinates
    ]
    
    d = r * acos(cos(phi2 - phi1) - cos(phi1) * cos(phi2) *
              (1 - cos(lambda2 - lambda1)))
    return d


def getDatabase():
    return countryData


def getSimilarity(headerList, name):
    candidates = []
    for header in headerList:
        headerName = header['name']
        if(name.lower() in headerName['common'].lower()):
            base = len(headerName['common'])
            restOfHit = len(headerName['common'].replace(name, ''))
            header['similarity'] = (base - restOfHit) / base
            candidates.append(header)

    candidates.sort(key=lambda x: x.get('similarity'), reverse=True)
    return candidates


class NameRetriever(Resource):

    def __init__(self):
        self.database = getDatabase()

    def get(self, name):
        candidates = getSimilarity(self.database, name)
        if(len(candidates) > 0):
            return candidates
        else: return 'No matched result'


class CountryList(Resource):

    def __init__(self):
        self.database = getDatabase()

    def get(self):
        nameSet = []
        for country in self.database:
            nameSet.append(country['name']['common'])
        return nameSet


class LocationRetriever(Resource):

    def __init__(self):
        self.database = getDatabase()

    def get(self, location):
        args = location.split(',')
        if (len(args) < 2): return 'Format error'
        source_lat = float(args[0])
        source_lng = float(args[1])
        max_distance = 1500
        candidates = []
        for country in self.database:
            target_loc = country['latlng']
            target_lat = target_loc[0]
            target_lng = target_loc[1]
            distance = getGeoDistance(source_lat, source_lng, target_lat, target_lng)
            if distance <= max_distance:
                country['distance'] = int(distance)
                candidates.append(country)
        candidates.sort(key=lambda x: x.get('distance'), reverse=False)
        for country in candidates:
            country['distance'] = str(country['distance']) + 'KM'
        return candidates


class DriveSideRetriever(Resource):

    def __init__(self):
        self.database = getDatabase()

    def get(self, drive_side):
        if drive_side.lower() not in ['left', 'right']:
            return 'drive side should be left or right'
        candidates = []
        for country in self.database:
            if country['car']['side'] == drive_side:
                candidates.append(country['name']['common'])
        return candidates

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)

api.add_resource(CountryList, '/country')
api.add_resource(NameRetriever, '/country/<name>')
api.add_resource(LocationRetriever, '/country/nearby/<location>')
api.add_resource(DriveSideRetriever, '/country/drive/<drive_side>')


if __name__ == '__main__':
    app.run(port=6001)

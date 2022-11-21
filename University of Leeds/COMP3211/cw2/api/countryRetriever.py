from fileOpt import getDatabase
from util import getGeoDistance
from flask_restful import Resource
from flask import request


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
        if (len(args) < 3): return 'Format error'
        source_lat = float(args[0])
        source_lng = float(args[1])
        max_distance =  float(args[2])
        candidates = []
        for country in self.database:
            target_loc = country['latlng']
            target_lat = target_loc[0]
            target_lng = target_loc[1]
            distance = getGeoDistance(source_lat, source_lng, target_lat, target_lng)
            if distance <= max_distance:
                country['distance'] = distance
                candidates.append({'name': country['name']['common'], 'distance': distance})
        candidates.sort(key=lambda x: x.get('distance'), reverse=False)
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
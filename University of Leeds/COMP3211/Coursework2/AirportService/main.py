from flask import Flask
from flask_restful import Resource, Api

import json
app = Flask(__name__)
api = Api(app)

class Airport(Resource):
    def __init__(self) -> None:
        super().__init__()
        with open('./AirportService/airport.json','r',encoding = 'utf-8') as fp: 
            self.data = json.load(fp) 

    def get(self,country_code):
        result = []
        for airport in self.data:
            if airport['country_code'].lower() == country_code.lower():
                result.append(airport)
        return result

api.add_resource(Airport, '/<string:country_code>')

if __name__ == '__main__':
    app.run(port=6002)

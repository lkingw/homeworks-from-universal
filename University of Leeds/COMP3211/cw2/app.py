from flask import Flask
from flask_restful import Api
from api import countryRetriever

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)

api.add_resource(countryRetriever.CountryList, '/country')
api.add_resource(countryRetriever.NameRetriever, '/country/<name>')
api.add_resource(countryRetriever.LocationRetriever, '/country/nearby/<location>')
api.add_resource(countryRetriever.DriveSideRetriever, '/country/drive/<drive_side>')

if __name__ == '__main__':
    app.run(debug=True)
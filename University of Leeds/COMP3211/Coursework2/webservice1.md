# Introduction

This project consists of an integrated client and three web services, here we only introduce the webservice 1.

## Webservice 1

The first web service as the basic service of our project is invoked and send according to that input connects to the country database. The country database is downloaded from https://restcountries.com/#api-endpoints-v3-all which contains basic attributes of all countries around the world including each country's location, currency, language, and so on.

This web service provides two kinds of restful route, the first one **/country/<name>** is designed to list all the matched countries and their attributes given a search text. To get better user experience, the retrieved countries will be ranked by the text similarity between search text and country name. If the user do not set the search text, it will list all countries's names.

As for the other route **/country/nearby/<lat,lon>**, it is designed to retrieve the nearby countries from a given location (in the form of coordinates). In this function, the half-side formula was selected to calculate the distance between coordinates entered and all countries list in our country database. Here, 1500KM was set as the maximum distance to define the "nearby". Given a <lat,lon> formated coordinates, this route will return all the countries meet the limitation of distance and the retrieved result will be ascending ordered by the distance.


# List of API routes
## Get a list of all countries
GET /country
Response example
```json
[
    "Mauritania",
    "Aruba",
    "Argentina",
    "Sweden",
    "Maldives",
    "Mexico"
]
```

## Get a list of countries that official name overlap the search text
GET /country/<name>
Response example
```json
[
    {
        "name": {
            "common": "China",
            "official": "People's Republic of China",
            "nativeName": {
                "zho": {
                    "official": "中华人民共和国",
                    "common": "中国"
                }
            }
        },
        "tld": [
            ".cn",
            ".中国",
            ".中國",
            ".公司",
            ".网络"
        ],
        "cca2": "CN",
        "ccn3": "156",
        "cca3": "CHN",
        "cioc": "CHN",
        "independent": true
        ...
    }
]
```

## Get a list of neighbouring countries in the given location (denoted by longitude and latitude) and distance
GET /country/nearby/<lat,lon,distance>
Response example
```json
[
    {
        "name": "China",
        "distance": 222.38985328911158
    },
    {
        "name": "Myanmar",
        "distance": 1403.5569285678869
    },
    {
        "name": "Mongolia",
        "distance": 1445.5340463792631
    },
    {
        "name": "Macau",
        "distance": 1468.680012230094
    }
]
```

# Dependencies
Python=3.9.11
Flask=2.2.2
Flask-RESTful=0.3.9

# How to run
python app.py
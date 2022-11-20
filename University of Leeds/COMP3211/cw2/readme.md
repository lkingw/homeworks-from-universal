# Project Introduction

This project consists of an integrated client and the following three web services:

> Webservice1 made by Your Name
Webservice2 made by XXX

The first web service is invoked and send according to that input connects to the country database. The database contains basic attributes of all countries around the world including each country's location, currency, language, and so on. This web service provides four kinds of restful APIs, the first one is used to list all the countries' names in our databases, and the second one is a query API, which is designed to list all the matched countries and their attributes given a search text. Different from the above APIs, this service also provides two more functional interfaces, one is designed to retrieve the nearby countries from the given location (in the form of coordinates), and the other is designed to retrieve the countries by the expected drive side.

> ...... to describe the other services

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

## Get a list of countries having same drive side
GET /country/drive/<drive_side>  
Response example
```json
[
    "Maldives",
    "New Zealand",
    "Pakistan",
    "Pitcairn Islands",
    "Zambia",
    "Seychelles",
    "Malaysia",
    "Christmas Island",
    "Singapore",
    "Suriname",
    "Ireland",
    "Australia",
    "Mauritius",
    "Papua New Guinea",
    "India",
    "Saint Lu
    ...
]
```

# Dependencies
Python=3.9.11
Flask=2.2.2
Flask-RESTful=0.3.9
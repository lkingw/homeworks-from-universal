Q1.1 Describe what the Web services composition does
Our service is designed to provide a user interface to help user check travel information of countries all over the world. Supported by the web serivice 1, the user can search countries by enter its name or partial name based on our country database. Besides, the user also can find the near by countries by enter their current location. After we get the perfered countries, leveraged by the web service 2, our service can list all the airports in selected country. Furthermore, with the extenal service, it is able to show all the flight infomation of each certain airport. Finally, we did a simple analysis of travel arrangements and feasibility.

Q1.2 Composition - Details

Web Service 1
Own or External: Own
Input: country name or geographical coordinates
Output: the detail information of country, if the input is geographical coordinates, the distance it will provided.
Output Parsing/Extraction of something of interest:
the result is a list of JSON object, we need the name, country code, and the geographical coordinates of each country.

Q3 Web Services Integration
In the homepage of our website, it is designed to receive user's input for country name or geographical coordinates. After we click the submit button, it will post the country name or geographical coordinates to web service 1, and the result will used to render country list view.
After the user click on the link after a country name, it will jumps to a view that present all the airports of the clicked country, that driven by the data from web service 2.
For the web service 3, then the user click the link after a airport name, it will take the user to airport view, which shows all the flights related on the seleted airport.


Q4 Web User Interface
We use flask Frameworks to develop both frontend and backend of this Web-based application. For the client, the website template is powered by Jinja2 engine, which can render a website with given variable value. We provide web routes as shown below.
1. GET '/index', render template 'index.html' which present the user inputs
2. POST '/index', render template 'country.html' to shows the searched countries.
3. GET '/airport?code={country_code}', render template 'airport.html' to display all the airport in selected country.
4. GET '/flight?iata={iata}', it render template 'flight.html' to present all the flight information of seleted airport.

Q1.1 Details
Name of the Web service
> Country service

Order in the workflow
> 1

Brief description
> The first web service as the basic service of our project is invoked and send according to that input connects to the country database. It can be used to check detail information of country and get nearby countries from given geographical coordinates.

Explain how the service is invoked.
> our service is powered by flask and flaskresful, based on it, we create two class named country retriever and location retriever and equip two get methods on them like the below code.
def get(self, name):
        candidates = getSimilarity(self.database, name)
        if(len(candidates) > 0):
            return candidates
        else: return 'No matched result'
When the user access the route '/country/<name>' or route '/country/nearby/<location>', the browser will execute thes methods and return reponses.

Measure the service invocation time
> With ten time experiments, the result said the average invocation time is 13.2ms and the std is 16.62.

Explain how you have obtained these mearements.
> We use postman to call this service and record the time cost for each time.
from flask import render_template, request, url_for, redirect, flash
from flask import Flask
import requests
 
ACCESS_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYjVjYjQ5ZWVlOWM1YTMzZmU2ZmNmZDhmMDY5Y2NlNjQ1ZDA2N2NkNzc2MmUyZjY2YTgxOWE0ZTE1YjVjZTQwODkyNDVmYWZmNzU2YzJkZGMiLCJpYXQiOjE2NjgzNDExMDksIm5iZiI6MTY2ODM0MTEwOSwiZXhwIjoxNjk5ODc3MTA5LCJzdWIiOiIxODAwNCIsInNjb3BlcyI6W119.MO-K-Y6AWWfXotZgfWdAN5wHMU2nN2OTsNKuuWSAlIAdG8FBvaGyWAYKR_Lf2hJ5ITTRPICRsO5PkwvD5dCJgw"

app = Flask(__name__)

@app.route('/index', methods=['GET','POST'])
def index():
    endpoint = "http://127.0.0.1:6001/country/"
    headers = {"User-Agent":"test request headers"}

    if request.method == 'POST':
        if request.form['type'] == 'byName' and len(request.form['country']) == 0:
            return redirect(url_for('index'))
        
        if request.form['type'] == 'byLocation' and (len(request.form['lat']) == 0 or len(request.form['lon']) == 0):
            return redirect(url_for('index'))

        if request.form['type'] == 'byName':
            country = request.form['country']
            headers = {"User-Agent":"test request headers"}
            r = requests.get(endpoint + country, headers=headers)
            return render_template('country.html', countries=r.json())
        
        if request.form['type'] == 'byLocation':
            lat = request.form['lat']
            lon = request.form['lon']
            r = requests.get(endpoint + 'nearby/' +  lat + ',' + lon, headers=headers)
            return render_template('country.html', countries=r.json())

    return render_template('index.html')

@app.route('/airport', methods=['GET']) 
def airport():    
    if "code" not in request.args or len(request.args['code']) == 0  :
        return redirect(url_for('index'))

    country_code = request.args['code']
    headers = {"User-Agent":"test request headers"}

    r = requests.get("http://127.0.0.1:6002/"+country_code,headers=headers)
    response = r.json()

    return render_template('airport.html',airports=response)

@app.route('/flight', methods=['GET']) 
def flight():
    if "iata" not in request.args or len(request.args['iata']) == 0  :
        return redirect(url_for('index'))
    depIata = request.args['iata']
    headers = {"User-Agent":"test request headers"}
    url = "https://app.goflightlabs.com/advanced-real-time-flights?access_key="+ACCESS_KEY+"&depIata="+depIata

    r = requests.get(url,headers=headers)
    response = r.json()

    flights = []
    if response['success'] and isinstance(response['data'],list):
        flights = response['data']
    return render_template('flight.html',flights=flights)
 
if __name__ == '__main__':
    app.run(port=8000,debug=True)

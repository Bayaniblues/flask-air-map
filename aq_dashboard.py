from flask import *
from flask_sqlalchemy import SQLAlchemy
import requests
import sqlite3 as sql
from functions import get_lat_array, get_long_array, unique_cities, search_city


app = Flask(__name__)
app.config.from_object(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    lastUpdate = DB.Column(DB.String(25))
    source = DB.Column(DB.String(100))
    value = DB.Column(DB.Float, nullable=False)
    parameter = DB.Column(DB.String(100))
    city = DB.Column(DB.String(100))
    lat = DB.Column(DB.Float, nullable=False)
    lon = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<Record {self.city}>'


@app.route('/search')
def show_user():
    list_cities = unique_cities()
    return render_template('search.html', data1=list_cities)


@app.route('/search/<city>')
def show_user_profile(city):
    city_in = city
    rows = search_city(city)

    return render_template('searchbeta.html',city_in=city_in, data1=rows)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data by using a functional method"""
    DB.drop_all()
    DB.create_all()

    headers = {'limit': '10000'}
    r = requests.get('https://api.openaq.org/v1/latest?limit=3000&country=US', headers=headers)
    for indexX, X in enumerate(r.json()['results']):
        for indexY, Y in enumerate(r.json()['results'][indexX]['measurements']):
            try:
                lastUpdate = r.json()['results'][indexX]['measurements'][indexY]['lastUpdated']
                source = r.json()['results'][indexX]['measurements'][indexY]['sourceName']

                value = r.json()['results'][indexX]['measurements'][indexY]['value']
                parameter = r.json()['results'][indexX]['measurements'][indexY]['parameter']

                city = r.json()['results'][indexX]['city']
                lat = r.json()['results'][indexX]['coordinates']['latitude']
                lon = r.json()['results'][indexX]['coordinates']['longitude']

                data = Record(
                              lastUpdate=lastUpdate,
                              source=source,
                              value=value,
                              parameter=parameter,
                              city=city,
                              lat=lat,
                              lon=lon)
                DB.session.add(data)
                DB.session.commit()

            except:
                continue

    return 'Data refreshed!'


@app.route('/')
def home():
    return render_template("/home.html")


@app.route('/lat')
def lat():
    return jsonify([1,2,3,4,5])


@app.route('/openaq')
def openaq():
    df1 = get_lat_array()
    df2 = get_long_array()
    return render_template("/openaq.html", data=json.dumps(df1), data2=json.dumps(df2))


if __name__ == '__main__':

    app.run(debug = True)


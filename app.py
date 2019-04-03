from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect database
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# save referenes
Measurement = Base.classes.measurement
Station = Base.classes.station

# create our session
session = Session(engine)
conn = engine.connect()

app = Flask(__name__)

@app.route("/")
def home():
    
    return(
        f"Welcome to the home page.<br> "
        f"<br>"
        f"Below are the available routes:<br>"
        f"<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prec():
    last_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-22').all()
    precipitation = list(np.ravel(last_year))
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    station_group = session.query(Measurement.station).\
        group_by(Measurement.station).all()
    stations = list(np.ravel(station_group))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year_temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter_by(station = 'USC00519281').filter(Measurement.date > '2016-08-22').all()
    temperature = list(np.ravel(last_year_temp))
    return jsonify(temperature)

@app.route("/api/v1.0/<start_date>")
def get_date(start_date):
    return jsonify (list(np.ravel(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= start_date).all())))

@app.route("/api/v1.0/<start_date>/<end_date>")
def end(start_date, end_date):
        ending = session.query((func.min(Measurement.tobs)), (func.avg(Measurement.tobs)), (func.max(Measurement.tobs))).\
        filter(Measurement.date <= end_date).filter(Measurement.date >= start_date).all()
        final2 = list(np.ravel(ending))
        return jsonify(final2)

if __name__ == '__main__':
    app.run(debug=True)
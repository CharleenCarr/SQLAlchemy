from __future__ import division

import datetime as dt
from datetime import date

import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/CharCarr/Documents/Data_Science/02-Homework/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

 # Create a dictionary from the row data and append to a list of all_passengers
    
   
@app.route("/")
def precip():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Please choose your vacation start date between the dates given and the same date format displayed 2017-08-23 and 2010-01-01.<br/>"
        f"/api/v1.0/<start><br/>"
        f"Please choose your vacation between the dates given and the same date format displayed 2017-08-23/2010-01-01.<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all station names"""
    # Query precipitation
    precip_query = session.query(Measurement.date, Measurement.prcp).all()

    precip_results = []
    for precip_result in precip_query:
        precip_dict = {}
        precip_dict[precip_result.date] = precip_result.prcp
        precip_results.append(precip_result)

    return jsonify(precip_results)

@app.route("/api/v1.0/station")
def station_names():
    """Return a list of all station names"""
    # Query all stations
    station_results = session.query(Station.name).all()

    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations from a year from the last data point"""
    # Query all temperatures
       
    prev_year = dt.date(year=2017, month=8, day=23)-dt.timedelta(days=365)

    tobs_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>=prev_year).order_by(Measurement.date.desc()).all()
    
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def trip1(start):

    start_date = pd.to_datetime(start)
    
    trip_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date.date()).all()    

    trip = list(np.ravel(trip_query))

    return jsonify(trip)
    
@app.route("/api/v1.0/<start>/<end>")
def trip2(start, end):

    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    travel_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start_date.date).filter(Measurement.date<=end_date.date).all()

    travel = list(np.ravel(travel_query))

    return jsonify(travel)

if __name__ == '__main__':  
    app.run(debug=True)

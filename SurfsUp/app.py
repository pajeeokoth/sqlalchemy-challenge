# Import the dependencies.
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a precipitationin the last 12 months"""
    # Query measurement table
    prcp_results = session.query(
        Measurement.prcp,
        #Measurement.station,
        Measurement.date).filter(Measurement.date > '2016-08-22').all()
    
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    precip = []
    for prcp, date in prcp_results:
        precip_dict = {}
        precip_dict["prcp"] = prcp
        precip_dict["date"] = date
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all stations
    station_results = session.query(Measurement.station).all()

    session.close()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the temperature observations for the most active station"""
    # Query all temperatures in the last year for most active station
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-22').filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = list(np.ravel(tobs_results))
    
    return jsonify(all_tobs)


@app.route("/api/v1.0/start_date/<date:start>")
def start_date(start):
    start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    """Return a precipitationin the last 12 months"""
    # Query measurement table
    t_sum = session.query(
        func.min(Measurement.tobs).label('tmin'),
        func.max(Measurement.tobs).lable('tavg'),
        func.avg(Measurement.tobs).label('max'))\
            .filter(Measurement.date > 'start').group_by('station').all()
    
    session.close()

 # Create a dictionary from the row data and append to a list of all_passengers
    temp_summ = []
    for tmin, tavg, tmax in t_sum:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_summ.append(temp_dict)


    return jsonify(temp_summ)

@app.route("/api/v1.0/start_end/<date:start>/<date:end>")
def start_end(start,end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the temperature observations for the most active station"""
    # Query all temperatures in the last year for most active station
    # Query measurement table
    t_summs= session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.max(Measurement.tobs).lable('TAVG'),
        func.avg(Measurement.tobs).label('TMAX'))\
            .filter(and_(Measurement.date > 'start',Measurement.date < 'end')).group_by('station').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = list(np.ravel(t_summs))
    
    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)

# Import the dependencies.
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        f"/api/v1.0/tobs"
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

if __name__ == '__main__':
    app.run(debug=True)

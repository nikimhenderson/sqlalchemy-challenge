# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
from datetime import date

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(stations = all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Calculate the date one year from the last date in data set
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        date_prcp.append(prcp_dict)

    return jsonify(date_prcp)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs for the past year for the most active station"""
    # Calculate the date one year from the last date in data set
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    # Query the dates and tobs of the most active station for previous year
    temp_obs_active = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= year_ago).\
                    filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(temp_obs_active))

    return jsonify(tobs = all_tobs)
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of minimum temperture, maximum temperature and avg temp for dates >= start date"""
    # Get input for start date
    start_dt = start
    # Query the min, max and avg tobs since start date
    min_max_avg = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_dt).all()

    session.close()

    # Convert list of tuples into normal list
    all_min_max_avg = list(np.ravel(min_max_avg))

    return jsonify(all_min_max_avg)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of minimum temperture, maximum temperature and avg temp for dates >= start date"""
    # Get input for start date
    start_dt = start
    end_dt = end
    # Query the min, max and avg tobs since start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start_dt).\
                    filter(Measurement.date <= end_dt).all()

    session.close()

    # Convert list of tuples into normal list
    all_min_max_avg = list(np.ravel(results))

    return jsonify(all_min_max_avg)

if __name__ == '__main__':
    app.run(debug=True)
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

measurement = Base.classes.measurement
station =Base.classes.station



# Calculate the date 1 year ago from the last data point in the database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# HINTS
# You will need to join the station and measurement tables for some of the queries.
# Use Flask jsonify to convert your API data into a valid JSON response object.



#/
# Home page.
# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"

    )

# /api/v1.0/precipitation route

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
# ---------------------JSON RESPONSE WORKED with ... /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary and Return the JSON"""
    session = Session(engine)
    prcp_results =session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all the precipitation for each date
    all_results= []
    for date, prcp in prcp_results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_results.append(date_dict)

    return jsonify(all_results)

#Return a JSON list of stations from the dataset. 
# -------------------------JSON list worked with /api/v1.0/stations-----------------------
@app.route("/api/v1.0/stations")
def stations():  
    """Return a JSON list of stations from the dataset.""" 
    session = Session(engine)
    results =session.query(station.name).all()
    session.close()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
 
# Query the dates and temperature observations of the most active station for the last year of data.
# tobs = session.query(measurement.date, measurement.tobs).filter(station.station =="USC00519281").filter(measurement.date >= prev_year).all()

# Return a JSON list of temperature observations (TOBS) for the previous year.
# -------------------------JSON list worked with /api/v1.0/tobs-----------------------

@app.route("/api/v1.0/tobs")
def tobs():  
    """Return a JSON list of temperature observations (TOBS) for the previous year.""" 
    session = Session(engine)
    tobs = session.query(measurement.date, measurement.tobs).filter(station.station =="USC00519281").filter(measurement.date >= prev_year).all()
    session.close()
    yearly_temp = []
    for date, temp in tobs:
        temp_dict ={}
        temp_dict["date"] =date
        temp_dict["TOBS"] =temp
        yearly_temp.append(temp_dict)
    return jsonify(yearly_temp)

@app.route("/api/v1.0/<start>/")
def start(start):
    """Return a JSON list of temperature observations (TOBS) for the given start and end dates."""
    from datetime import datetime
    # date example for datetime input method,      start = '2016-08-23'
    start = datetime.strptime(start, "%Y-%m-%d")
    session =Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
    .filter(measurement.date >= start).all()
    session.close()
    # temp = list(np.ravel(results))
    tobs_obs =[]
    for min, average, max in results:
        obs_dict ={}
        obs_dict["min temp"] = min
        obs_dict["average temp"] =average
        obs_dict["Max temp"] = max
        tobs_obs.append(obs_dict)
    return jsonify(tobs_obs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# start = dt.date(2015, 6, 1)
# end = dt.date(2016, 12, 1) 

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return a JSON list of temperature observations (TOBS) for the given start and end dates."""
    from datetime import datetime
    start = datetime.strptime(start, "%Y-%m-%d")
    end =datetime.strptime(end, '%Y-%m-%d')
    session =Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
    .filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    # temp = list(np.ravel(results))
    tobs_obs =[]
    for min, average, max in results:
        obs_dict ={}
        obs_dict["min temp"] = min
        obs_dict["average temp"] =average
        obs_dict["Max temp"] = max
        tobs_obs.append(obs_dict)
    return jsonify(tobs_obs)
 

if __name__ == '__main__':
    app.run(debug=True)    


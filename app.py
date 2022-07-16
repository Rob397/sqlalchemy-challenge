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
station =Base.classes.stationer



# Calculate the date 1 year ago from the last data point in the database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


#/
# Home page.
# List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )

# /api/v1.0/precipitation route

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
        """Convert the query results to a dictionary and Return the JSON"""
        session = Session(engine)
        prcp_results =session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
        session.close()
        # Create a dictionary from the row data and append to a list of all the precipitation for each date
        precip_results= = []
    for date, prcp in prcp_results:
        date_dict = {}
        date_dict["prcp"] = prcp
        precip_results.append(date_dict)

    return jsonify(prcp_results)


    




# Example
# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)





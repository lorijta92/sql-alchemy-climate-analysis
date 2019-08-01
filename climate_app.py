import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy import and_

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references
Measurement = Base.classes.measurement
Stations = Base.classes.station



# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return (
    f"<h2>Welcome to the Hawaii Climate App.</h2><br/>"
    f"Available routes are:<br/>"
    f"<ul><li>Precipitation - <code>/api/v1.0/precipitation</code></li></ul>"
    f"<ul><li>Stations - <code>/api/v1.0/stations</code></li></ul>"
    f"<ul><li>Temperature Observations - <code>/api/v1.0/tobs</code></li></ul>"
    f"<ul><li>Start - <code>/api/v1.0/<start></code></li></ul>"
    f"<ul><li>Start and End - <code>/api/v1.0/<start>/<end></code></li></ul>")

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query dates and precipitation
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary using 'date' as the key and 'prcp' as the value
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict) 

    session.close() #close session before return

    return jsonify(prcp_list)
    
    # "finally: session.close()" - 'finally' used after exceptions, no need for it if not using exception
    

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurement.station).distinct().all()
    
    stations_list = list(np.ravel(results))

    session.close()

    return jsonify(stations_list)


# Temperature Observation Routes
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query dates
    session = Session(engine)
    dates = session.query(Measurement.date).all()
    
    last_date = dates[-1][0]
    end_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    end_dt = end_dt.date()
    start_dt = end_dt - dt.timedelta(days=365)
    
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>=start_dt).\
        filter(Measurement.date<=end_dt).all()
    
    session.close()

    return jsonify(tobs)



# TMIN, TAVG, TMAX with only start date
@app.route("/api/v1.0/<start>")
def start(start):
    
    # Query dates and temperature observations
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()

    # Create empty list to hold dates and temperature observations
    tobs_list = []

    # Create empty list to hold minimum temperature, average temperature, and maximum temperature
    temps_list = []

    # Use for loop to append the empty tobs_list with dictionaries of dates and temperature observations
    for date, temp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = temp
        tobs_list.append(tobs_dict) 

    # Use for loop to iterate through the list and set the value of search_term
    for item in tobs_list:
        search_term = item["date"]
    
        # If the search term is the same as the argument inputted by the user
        # Calculate TMIN, TAVG, TMAX  for all dates greater than or equal to the argument
        if search_term == start:
            calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

            # Store calculations in a list and return as a JSON object
            for tmin, tavg, tmax in calc_temps:
                temps_dict = {}
                temps_dict["Minimum Temperature"] = tmin 
                temps_dict["Average Temperature"] = tavg
                temps_dict["Maximum Temperature"] = tmax
                temps_list.append(temps_dict)

            return jsonify(temps_list)

    session.close()

    # Return error message if the date inputted by the user is not apart of the data set
    return jsonify({"error": f"The date {start} was not found."}), 404



# TMIN, TAVG, TMAX with start and end dates
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    # Query dates and temperature observations
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()

    tobs_list = []
    temps_list = []

    for date, temp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = temp
        tobs_list.append(tobs_dict) 

    for item in tobs_list:
        search_term = item["date"]

    if all(i in tobs_list for i in (start, end)):
        calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        for tmin, tavg, tmax in calc_temps:
            temps_dict = {}
            temps_dict["Minimum Temperature"] = tmin 
            temps_dict["Average Temperature"] = tavg
            temps_dict["Maximum Temperature"] = tmax
            temps_list.append(temps_dict)

        return jsonify(temps_list)

    session.close()

    return jsonify({"error": f"The dates {start} and {end} were not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
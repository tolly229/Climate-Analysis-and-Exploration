import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Climate Analysis and Exploration<br/><br/>"
    
        f"Avalable Routes:<br/><br/>"
        
        f"/api/v1.0/precipitation<br/>"
        f"- Dates and Temperature Observations from last year<br/><br/>"
        
        f"/api/v1.0/stations<br/>"
        f"- List of stations from the dataset<br/><br/>"

        f"/api/v1.0/tobs<br/>"
        f"- List of temperature observations (tobs) from the previous year<br/><br/>"

        f"/api/v1.0/START DATE GOES HERE<br/>"
        f"- List of min, avg, and max temperature for a given start date<br/><br/>"
        
        f"/api/v1.0/START DATE GOES HERE/END DATE GOES HERE<br/>"
        f"- List of min, avg, and max temperature for a given start/end range<br/><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prec =session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()
    precipitation_dict = dict(prec)
    session.close()
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    station =session.query(Station.station).all()
    station_list=[]
    for item in station:
        station_list.append("".join(item))
    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tob =session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()
    tob_dict = dict(tob)
    session.close()
    return jsonify(tob_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    custom_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()
    return jsonify(custom_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    custom_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    custom_end = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date <= end).all()
    session.close()
    return jsonify(custom_start,custom_end)


if __name__=='__main__':
    app.run(debug=True)



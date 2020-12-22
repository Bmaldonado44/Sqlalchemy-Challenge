import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base= automap_base()
Base.prepare(engine, reflect=True)
measurements = Base.classes.measurement
stations = Base.classes.station
session = Session(engine)

@app.route("/")
def home():
    output = ('<h3>copy bottom links to url to get results:</h3>' 
            '<ul><li>/api/v1.0/precipitation</li>' 
            '<li>/api/v1.0/stations</li>' 
            '<li>/api/v1.0/tobs</li>' 
            '<li>/api/v1.0/<start> and /api/v1.0/<start>/<end></li></ul>')
    return output

@app.route('/api/v1.0/precipitation')
def precipitation():
    precip = session.query(measurements.date, measurements.prcp).all()
    return { date : prcp for date, prcp in precip }

@app.route('/api/v1.0/stations')
def stn():
    stns = session.query(stations.name).all()
    return pd.DataFrame(stns).to_json()



if __name__ == "__main__":
    app.run(debug=True)

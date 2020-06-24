"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request
from werkzeug import secure_filename
from SPKTOPSIS import app
from SPKTOPSIS.Controller.SPK import topsis
from io import StringIO
import pandas as pd

@app.route('/')

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Kelompok 1',
        year=datetime.now().year,
    )

@app.route('/spk', methods=['GET','POST'])
def spk():
    if request.method == "POST":
        f = request.files['data']
        data = pd.read_csv(f)

        w = request.files['weight']
        weight = pd.read_csv(w)

        upload = True
    else:
        upload = False
        data = r'SPKTOPSIS\static\content\data.csv'
        weight = r'SPKTOPSIS\static\content\weight.csv'

    """Renders the SPK page."""
    return render_template(
        'spk.html',
        title='SPK Topsis',
        year=2020,
        datas= topsis(data,weight,upload),
        upload= upload
    )

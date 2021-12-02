"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request
from SPKTOPSIS import app
from SPKTOPSIS.Controller.SPK import topsis
from io import StringIO
import pandas as pd

@app.route('/', methods=['GET','POST'])
def spk():
    msg = ""
    if request.method == "POST":
        upload = True

        f = request.files['data']
        data = pd.read_csv(f)

        w = request.files['weight']
        weight = pd.read_csv(w)

        datas = topsis(data,weight,upload)
        if(datas == False):
            msg = "Jumlah Kriteria pada data dan weight berbeda."
            
    else:
        upload = False
        data = r'SPKTOPSIS\static\content\data.csv'
        weight = r'SPKTOPSIS\static\content\weight.csv'

        datas = topsis(data,weight,upload)

    """Renders the SPK page."""
    return render_template(
        'spk.html',
        title='DSS Topsis',
        year=2020,
        datas= datas,
        upload= upload,
        msg = msg
    )

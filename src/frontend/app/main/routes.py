from app.main import bp
from flask import render_template

import pandas as pd
import json

@bp.route('/')
@bp.route('/index')
def index():
    df = pd.read_csv('/Users/kyleong/insight/proj/frontend/app/main/data.csv').drop('Open', axis=1)

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}

    title_data = {"text": "Reddit Trends"}

    return render_template("index.html", data=data, title=title_data)
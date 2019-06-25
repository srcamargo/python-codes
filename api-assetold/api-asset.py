from flask import Flask, render_template,send_file, request, make_response, session
import pandas_datareader as pdr
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import datetime
from io import BytesIO
plt.style.use('ggplot')
import threading


app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

@app.route('/web/')
def web():
    asset = request.args.get('asset')
    if not asset:
    #    asset = 'BBAS3.SA'
        asset = session.get('asset')

    plt.clf()
    ms=pdr.get_data_yahoo(asset,start=datetime.datetime(2018,6,18),end=datetime.datetime(2019,6,21))
    #ms = ms.asfreq('B')
    ms['MA8'] = ms['Close'].rolling(10).mean()
    ms['MA20'] = ms['Close'].rolling(50).mean()
    ms = ms.dropna()
    plt.title(session['asset'])

    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing price ($)')
    #ax.set_xticklabels(ms.index)
    ax.plot(ms.index,ms['Close'],label=asset)
    ax.plot(ms.index,ms['MA8'],label='Moving Average 8')
    ax.plot(ms.index,ms['MA20'],label='Moving Average 20')
    ax.legend()
    plt.xticks(rotation=60)
    plt.plot()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.autofmt_xdate()
    fig = plt.savefig(img)
    plt.clf()
    plt.cla()
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')
	
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    #session.pop('asset',None)
    #session['asset'] = request.args.get('asset')
    asset = request.args.get('asset')
    if not asset:
        asset = 'BTC-USD'
	
    session['asset'] = asset
    return render_template('index.html',asset=session['asset'])
	
	
if __name__ == '__main__':

    app.run(debug=True, host = '0.0.0.0')
	
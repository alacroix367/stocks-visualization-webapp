#Load the packages
from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.models import Legend
from bokeh.plotting import figure, show
from bokeh.models.formatters import DatetimeTickFormatter
import pandas as pd
import numpy as np
import requests
import simplejson
from datetime import datetime

#Connect the app
app = Flask(__name__)
vars = {}

@app.route('/index',methods = ['GET','POST'])
def index():
  if request.method=='GET':
    return render_template('index_SV.html')
  else:
    #########################################
    ### Save user inputs to app.vars dict ###
    #########################################
    ticker = request.form['ticker_lulu']
    varnames = ['uOpen','uClose','open','close']
    for vn in varnames:
      try:
        vars[vn] = request.form[vn+'_lulu']
      except:
        vars[vn] = 0

    ###########################################
    ### Get data from API into pd.DataFrame ###
    ###########################################
    iexbaseURL = 'https://cloud.iexapis.com/beta/stock/'
    daterange = '1y'
    iexAPIkey = 'pk_6ec02dfdbdbe4fcca1839538772ea7d8'
    fullURL = iexbaseURL + ticker + '/chart/' + daterange + '/quote?token=' + iexAPIkey
    response = requests.get(fullURL)
    df = pd.DataFrame(response.json())

    ####################################################################
    ### Convert date column to datetime format compatible with Bokeh ###
    ####################################################################
    def to_datetime(val):
      y, m, d = val.split('-')
      return datetime(int(y),int(m),int(d))
    df['date']=df.date.map(to_datetime)

    ##################################################################
    ############ Figure out which columns we're plotting #############
    ### What variable names correspond to descriptive column names ###
    ##################################################################
    columnsdict = {'open': 'Adjusted Opening Price',\
                   'close': 'Adjusted Closing Price',\
                   'uOpen': 'Unadjusted Opening Price',\
                   'uClose': 'Unadjusted Closing Price'}
    ys = [vn for vn in vars if vars[vn]!=0] # ys to plot
    columnslist = [columnsdict[y] for y in ys] # for legend

    ################################
    ### Put together plot itself ###
    ################################
    clrs = ["firebrick","navy","mediumseagreen","grey"]
    plt = figure(plot_width=600, plot_height=500, title = "IEXcloud Stock Prices - 2018")
    for p in range(len(ys)):
      plt.line(df['date'],df[ys[p]],\
           color = clrs[p],\
           alpha = 0.8,\
           line_width=1.5,\
           legend = ticker + ": " + columnslist[p])
      plt.xaxis.formatter = DatetimeTickFormatter(months = '%b %y')
      plt.xaxis.axis_label = "Date"
      plt.yaxis.axis_label = "Price $"
      plt.legend.location = "top_right"

    script, div = components(plt)

    #Render the page
    return render_template('home_SV.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
#  app.run(debug=True)
#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
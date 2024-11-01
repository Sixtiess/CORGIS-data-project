from flask import Flask, request, render_template, flash
from markupsafe import Markup
from datetime import datetime

import os
import json

app = Flask(__name__)

@app.route('/')
def render_about():
    return render_template('home.html')

@app.route('/delaybyairport')
def render_delaybyairport():
    options = ""
    with open('airlines.json') as airlines_data:
        months = json.load(airlines_data)
        
    if "airport" in request.args:
        airport = request.args['airport']
        
        maxNum = 0
        numMonth = ""
        maxMinutes = 0
        minutesMonth = ""
        for i in months:
            if i["Airport"]["Code"] == airport:
                if i["Statistics"]["Minutes Delayed"]["Total"] > maxMinutes:
                    maxMinutes = i["Statistics"]["Minutes Delayed"]["Total"]
                    minutesMonth = i["Time"]["Month Name"]+" of "+str(i["Time"]["Year"])
                if i["Statistics"]["Flights"]["Delayed"] > maxNum:
                    maxNum = i["Statistics"]["Flights"]["Delayed"]
                    numMonth = i["Time"]["Month Name"]+" of "+str(i["Time"]["Year"])
        for i in range(0,152):
            options += Markup("<option value=\"" + months[i]["Airport"]["Code"] + "\">" + months[i]["Airport"]["Name"] + "</option>")
        return render_template('mostDelayedMonthResponse.html', options=options,maxNum1=maxNum,numMonth1=numMonth,maxMinutes1=maxMinutes,minutesMonth1=minutesMonth)
    
    for i in range(0,29):
        options += Markup("<option value=\"" + months[i]["Airport"]["Code"] + "\">" + months[i]["Airport"]["Name"] + "</option>")
    return render_template("mostDelayedMonth.html",options=options)
    

@app.route('/delaybytime')
def render_delaybytime():
    options = ""
    with open('airlines.json') as airlines_data:
        months = json.load(airlines_data)
        
    if "month" in request.args:
        month = request.args['month']
        
        maxNum = 0
        numAirport = ""
        maxMinutes = 0
        minutesAirport = ""
        for i in months:
            if i["Time"]["Label"] == month:
                if i["Statistics"]["Minutes Delayed"]["Total"] > maxMinutes:
                    maxMinutes = i["Statistics"]["Minutes Delayed"]["Total"]
                    minutesAirport = i["Airport"]["Name"]
                if i["Statistics"]["Flights"]["Delayed"] > maxNum:
                    maxNum = i["Statistics"]["Flights"]["Delayed"]
                    numAirport = i["Airport"]["Name"]
        for i in range(0,152):
            options += Markup("<option value=\"" + months[i*29]["Time"]["Label"] + "\">" + months[i*29]["Time"]["Label"] + "</option>")
        return render_template('mostDelayedAirportResponse.html', options=options,maxNum1=maxNum,numAirport1=numAirport,maxMinutes1=maxMinutes,minutesAirport1=minutesAirport)
    
    for i in range(0,152):
        options += Markup("<option value=\"" + months[i*29]["Time"]["Label"] + "\">" + months[i*29]["Time"]["Label"] + "</option>")
    return render_template("mostDelayedAirport.html",options=options)


@app.route('/delaysovertime')
def render_delaysovertime():
    options = ""
    with open('airlines.json') as airlines_data:
        months = json.load(airlines_data)
    
    if "airport" in request.args:
        airport = request.args['airport']
        chartAdd = ""
        airportName = ""
        for n in months:
            if n["Airport"]["Code"] == airport:
                chartAdd += Markup("{ label: '"+str(n["Time"]["Label"])+"',  y: "+str(n["Statistics"]["Flights"]["Delayed"])+"  },")
                airportName = n["Airport"]["Name"]
        for i in range(0,29):
            options += Markup("<option value=\"" + months[i]["Airport"]["Code"] + "\">" + months[i]["Airport"]["Name"] + "</option>")
        txt = "Delays at "+airportName+" over time"
        return render_template("delaysOverTimeResponse.html",options=options,chartAdd1=chartAdd,titleText=txt)
        
    for i in range(0,29):
        options += Markup("<option value=\"" + months[i]["Airport"]["Code"] + "\">" + months[i]["Airport"]["Name"] + "</option>")    
    return render_template("delaysOverTime.html",options=options)
    
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False)

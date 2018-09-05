from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from weather import Weather
from pprint import pprint
import requests

#
# client = Client("AC193c5eb63ec1425bfa176660f0dbce2d", "5f822f7cd8eed94719b711bfa77fa8a8")
#
# client.messages.create(to="+17818792907",
#                       from_="+19597774928",
#                        body="Hi maureen please respond to this with a simple response for i am not yet programmed for advanced input. Exp: Hello,hello,hi,Hi")
#

def getWeather(place):
    weekly_Summary = []
    weather = Weather()
    location = weather.lookup_by_location(str(place))
    condition = location.condition()
    print('\n')
    forecasts = location.forecast()
    for forecast in forecasts:
        weekly_Summary.append(forecast.date()+" Weather: "+forecast.text()+" High: "+forecast.high()+" Low: "+forecast.low()+"")
    wind = location.wind()
    now = location.condition()
    output = "Current Weather:\n" \
             "Temperature: "+now.temp()+" \
             ""\nGeneral: "+now.text()+" \
             ""\nWind Info: "+str(wind)+" " \
             " \nWeekly Summary: "+ str(weekly_Summary)+""

    return print(output)


getWeather("west hartford")


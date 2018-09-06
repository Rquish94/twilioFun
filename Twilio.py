from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from weather import Weather
from pprint import pprint
import requests



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


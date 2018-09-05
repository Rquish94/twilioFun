import whois
import time
import requests
from flask import Flask, Response, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from weather import Weather
from pprint import pprint
import requests
weather = Weather()

num = int


app = Flask(__name__)


def zipSplit(string):
    zip = string.rstrip('0123456789')
    town = string[len(zip):]
    return zip, town
#Used to seperate zipcode from text
# zip, notNeeded = zipSplit(mod_inbound)


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

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = MessagingResponse()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    mod_inbound = str(inbound_message).lower()
    # we can now use the incoming message text in our Python application
    if mod_inbound == "xmr" or mod_inbound == "monero":
        response.message('Hi gretchen! this is specialized for you! cause you just gave me a simple reponse... imagen what i could grab from the web lightining fast for ya')

    elif "weather" in mod_inbound:
        mod_resp = str(mod_inbound).replace("weather",'')
        response.message(getWeather(mod_resp))

    elif "whois" in mod_inbound:
        mes_resp = str(mod_inbound).replace("whois",'')
        lookup = whois.whois(mes_resp)
        response.message(lookup)

    else:
        response.message("Hi! Not quite sure what you meant, but okay.")
    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


if __name__ == "__main__":
    app.run(debug=True)
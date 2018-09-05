import whois
from flask import Flask, Response, request
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from weather import Weather
from pprint import pprint
import re
import requests
weather = Weather()


app = Flask(__name__)


def zipSplit(string):
    zip = string.rstrip('0123456789')
    town = string[len(zip):]
    return zip, town
#Used to seperate zipcode from text
# zip, notNeeded = zipSplit(mod_inbound)


def distance(original, destination):
    distance_API_KEY = 'AIzaSyDYySzpPkj2WDGrOwME2LTC3b5yBBHN4NQ'
    # org = '25+arden+road+west+hartford+connecticut'
    # dest = 'cocc+southington+ct'
    url2 = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + original + '&destinations=' + destination + '&key=' + distance_API_KEY + ''
    d = requests.get(url2).text
    print(d)
    texts = re.findall('("text" :)\s(.*)', d)
    print(texts)
    output = (str(texts).replace('(', '').replace(')', '').replace('text', '').replace("'", '').replace('"', '').replace(':','').replace(',', '').replace("]", '').replace('[', '').split('km'))
    print(output)
    miles = float(str(output[0])) / 1.609344
    return str(miles) + " miles " + output[1]


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
    current_output = "Current Weather:\n" \
             "Temperature: "+now.temp()+" \
             ""\nGeneral: "+now.text()+" \
             ""\nWind Info: "+str(wind)+" " \

    weekly_output = "Weekly Summary: "+ str(weekly_Summary)

    return current_output,weekly_output

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = MessagingResponse()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    mod_inbound = str(inbound_message).lower().split(' ')
    print(mod_inbound)
    # we can now use the incoming message text in our Python application
    if mod_inbound == "xmr" or mod_inbound == "monero":
        response.message('This was originally meant to remotely trade crypto')

    elif  "weekly" in (mod_inbound)[0] and "weather" in (mod_inbound)[1]:
        str_mod_inbound = str(mod_inbound).replace(",","").replace("[","").replace("]","").replace("'","")
        print(str_mod_inbound)
        mod_resp = str(str_mod_inbound).replace("weekly",'').replace("weekly weather",'')
        daily,weekly = getWeather(mod_resp)
        response.message(weekly)
    elif "distance" in (mod_inbound)[0]:
        str_mod_inbound = str(mod_inbound).replace(",", "").replace("[", "").replace("]", "").replace("'", "")
        print(str_mod_inbound)
        inputstuff = str(str_mod_inbound).replace("distance",'').replace('too','to').split('to')
        response.message(distance(inputstuff[0],inputstuff[1]))
    elif "weekly" in (mod_inbound)[0]:
        str_mod_inbound = str(mod_inbound).replace(",","").replace("[","").replace("]","").replace("'","")
        print(str_mod_inbound)
        mod_resp = str(str_mod_inbound).replace("weekly", '').replace("weekly weather", '')
        daily, weekly = getWeather(mod_resp)
        response.message(weekly)
    elif "weather" in (mod_inbound)[0]:
        str_mod_inbound = str(mod_inbound).replace(",","").replace("[","").replace("]","").replace("'","")
        print(str_mod_inbound)
        mod_resp = str(str_mod_inbound).replace("weather", '')
        daily, weekly = getWeather(mod_resp)
        response.message(daily)
    elif "whois" in mod_inbound[0]:
        data = []
        mes_resp = str(mod_inbound).replace("whois",'').replace(' ','').replace(']','').replace("'",'').split(',')
        lookup = whois.whois(str(mes_resp[1]))
        for line in lookup:
            data.append(str(line)+" ==> "+str(lookup[line]))
        print(len(str(data)))
        response.message(str(data))
    elif ";)" in (mod_inbound)[0]:
        response.message("Hi gretchen ;)")

    else:
        response.message("Please only send me texts that contain the following: the word weather followed by a location for current weather or the word weekly followed by a location for weekly weather. E.g.: weather san juan")
    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200

if __name__ == "__main__":
    app.run(debug=True)
import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Open Weather Map
OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast?"
API_KEY = os.environ.get("OWM_KEY")
LAT = 40.712776
LON = -74.005974

# Twilio
account_sid = "ACe6fdb96386238b8f80893e15bc457b7a"
auth_token = os.environ.get("TWILIO_TOKEN")

params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
}
res = requests.get(OWM_endpoint, params=params)
res.raise_for_status()

# Weather data for next 12hrs with a 3hr step
# (3hr step is determined by OWM free subscription)
weather_data = res.json()["list"][:5]

will_rain = False
# Check weather for every 3hrs for next 12hrs
for weather in weather_data:
    code = weather["weather"][0]["id"]

    if code < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        to="+16466629576",
        from_="+18446480994",
        body="Its going to rain today! ☔"
    )

    print(message.status)




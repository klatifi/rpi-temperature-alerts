#!/usr/bin/python

import time
import json
import sendgrid
import Adafruit_DHT

# Get Config
with open('config.json') as config_file:
  config = json.load(config_file)

# Setup
thresh = config["temperatureThreshold"]  # Temperature threshold to send alert
timeout = config["timeout"] # Minutes between tries
sensor = Adafruit_DHT.DHT11
pin = config["sensorPin"] # Sensor pin
humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
sg = sendgrid.SendGridAPIClient(apikey=config["apiKey"]) # Set SendGrid API key

def sendMail(data):
  response = sg.client.mail.send.post(request_body=data)
  if response.status_code == 202:
    print "Mail sent okay!"
  else:
    print "Mail unable to be sent, see the following:"
    print(response.status_code)
    print(response.body)
    print(response.headers)

# Loop
while True:
  if temp is not None:
    if temp > thresh:
      print('Temp high! Temp: {0:0.1f}*C  Humidity: {1:0.1f}%'.format(temp, humidity))
      data = {"personalizations":[{
          "to":[{"email": config["emailTo"]}],
          "subject": "Temperature Sensor Warning!"
        }],
        "from": {"email": config["emailFrom"]},
        "content": [{
          "type": "text/plain",
          "value": "Temperature alert threshold of " + str(thresh) + "*C has been reached. Current reading: " + str(temp) + "*C."
      }]}
      sendMail(data)
    else: 
      print "Below thresh: " + str(temp)
  else:
    print('Failed to get reading. Try again!')
    data = {"personalizations":[{
        "to":[{"email": config["emailTo"]}],
        "subject": "Temperature Sensor Warning!"
      }],
      "from": {"email": config["emailFrom"]},
      "content": [{
        "type": "text/plain",
        "value": "Failed to get temperature sensor reading. Please investigate!"
    }]}
    sendMail(data)

  time.sleep(60 * timeout) # Wait for a while to stop email spam

#!/usr/bin/python

import json
import Adafruit_DHT

# Get config
with open('config.json') as config_file:
  config = json.load(config_file)

# Setup
sensor = Adafruit_DHT.DHT11
pin = config["sensorPin"]
humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, humidity))

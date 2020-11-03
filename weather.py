import argparse
import time
import datetime
from datetime import datetime
import paho.mqtt.client as mqtt #import the client1
import epics
from epics import camonitor
from epics import PV

parser = argparse.ArgumentParser()
#parser.add_argument("-b", "--broker", default="localhost", help="host running the MQTT broker service")

args = parser.parse_args()

broker_address=args.broker
client = mqtt.Client("ca-weather") #create new instance
client.connect(broker_address) #connect to broker
client.subscribe("ukirt/weather/#")

def pub_as_influxdb(value, posixseconds, nanoseconds, measurement="weather", location="ukirt", sensor="wind", units="mph"):
  line="%s,location=%s,sensor=%s,units=%s speed=%s %.0f%d"%(measurement, location, sensor, units, value, posixseconds, nanoseconds)
  client.publish("ukirt/weather/wind/speed",line)
  print(line)
 
def cb_wind_speed(pvname=None, timestamp=None, char_value=None, value=None, units=None, host=None, **kw):
  if pvname == 'ws:wind_spd:val':
    #print(pvWS.info)
    pub_as_influxdb(pvWS.char_value,pvWS.posixseconds,pvWS.nanoseconds)
  

pvWS = PV('ws:wind_spd:val')
print(pvWS.info)

camonitor('ws:wind_spd:val', callback=cb_wind_speed)

time.sleep(60*5)      # run for 5 minutes

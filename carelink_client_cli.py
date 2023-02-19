#!/usr/bin/python
# -*- coding: ascii -*-

import carelink_client
import argparse
import datetime
import time
import json
from asciichartpy import plot
import asciichartpy
import os
from dotenv import load_dotenv

load_dotenv()


def writeJson(jsonobj, name):
   filename = name + "-" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
   try:
      f = open(filename, "w")
      f.write(json.dumps(jsonobj,indent=3))
      f.close()
   except Exception as e:
      print("Error saving " + filename + ": " + str(e))
      return False
   else:
      return True

def graphdata(json):
  # returns JSON object as
  # a dictionary
  data = json

  last_day_values = []
  color_list = []
  x = []
  counter = 0

  # Clear the term
  os.system('cls' if os.name == 'nt' else 'clear')

  # Set all values for for-loop to empty
  normal_bucket = []
  high_bucket = []
  low_bucket = []
  high_line = []
  low_line = []
  counter = 0

  for i in data['sgs']:
    # Drop the oldest value if we already have 60
    # if counter >= 100:
    #   normal_bucket.pop(0)
    #   high_bucket.pop(0)
    #   low_bucket.pop(0)
    #   high_line.pop(0)
    #   low_line.pop(0)

    # We want to bucket data as much as we can
    # Each bucket has to match in size in order to color it appropriately
    # So, we fill each bucket with a null value if it does not belong so that
    # we can move the values along with each other. If they were of different
    # size then they would all start at x = 0 where the bucket begins
    current_value = int(i['sg'])

    if current_value == 0:
      normal_bucket.append(float("nan"))
      high_bucket.append(float("nan"))
      low_bucket.append(float("nan"))
    elif current_value > 180:
      normal_bucket.append(float("nan"))
      high_bucket.append(current_value)
      low_bucket.append(float("nan"))
    elif current_value < 70:
      normal_bucket.append(float("nan"))
      high_bucket.append(float("nan"))
      low_bucket.append(current_value)
    else:
      normal_bucket.append(current_value)
      high_bucket.append(float("nan"))
      low_bucket.append(float("nan"))

    high_line.append(180)
    low_line.append(70)
    counter += 1

    last_day_values = [normal_bucket, high_bucket, low_bucket, high_line, low_line]
    color_list = [asciichartpy.green, asciichartpy.lightmagenta, asciichartpy.red, asciichartpy.lightyellow , asciichartpy.lightred]

    # Clear and print every time we get a value
    # os.system('cls' if os.name == 'nt' else 'clear')
    # print(plot(last_day_values, {'height':15, 'colors': color_list, 'min': 35, 'max': 200}))

  # Print the graph at the end (faster)
  print(plot(last_day_values, {'height':35, 'colors': color_list, 'min': 35}))


  # Print some more useful info that we want:
  # Get hours with floor division
  hours = data['timeToNextCalibrationMinutes'] // 60
  # Get additional minutes with modulus
  minutes = data['timeToNextCalibrationMinutes'] % 60

  print('\n####################################################')
  print('BG Info:')
  print('  Last Value: %i' % (data['lastSG']['sg']))
  print('    Recorded at: %s' % (data['lastSG']['datetime']))
  print('  Time In Range (24 hours): %i %%' % (data['timeInRange']))
  print('Sensor Info:')
  print('  Status: %s' % (data['calibStatus']))
  print('  Time to Next Calibration: %d h and %d min' % (hours, minutes))
  print('  Battery Percentage: %i %%' % (data['gstBatteryLevel']))
  print('Pump Info:')
  print('  Battery Percentage: %i %%' % (data['medicalDeviceBatteryLevelPercent']))
  print('  Approx Remaining Units of Insulin: %f u' %(data['reservoirRemainingUnits']))
  print('####################################################')


# Parse command line
parser = argparse.ArgumentParser()
parser.add_argument('--username', '-u', type=str, help='CareLink username', required=False, default=os.getenv('MED_USERNAME'))
parser.add_argument('--password', '-p', type=str, help='CareLink password', required=False, default=os.getenv('MED_PASSWORD'))
parser.add_argument('--country',  '-c', type=str, help='CareLink two letter country code', required=False, default=os.getenv('MED_COUNTRY'))
parser.add_argument('--repeat',   '-r', type=int, help='Repeat request times', required=False)
parser.add_argument('--wait',     '-w', type=int, help='Wait minutes between repeated calls', required=False)
parser.add_argument('--data',     '-d', help='Save recent data', action='store_true')
parser.add_argument('--verbose',  '-v', help='Verbose mode', action='store_true')
parser.add_argument('--plotter',  '-z', help='Terminal plot mode (instead of downloading)', action='store_true')
args = parser.parse_args()

# Get parameters
username = args.username
password = args.password
country  = args.country
repeat   = 1 if args.repeat == None else args.repeat
wait     = 5 if args.wait == None else args.wait
data     = args.data
verbose  = args.verbose
plotter  = args.plotter

#print("username = " + username)
#print("password = " + password)
#print("country  = " + country)
#print("repeat   = " + str(repeat))
#print("wait     = " + str(wait))
#print("data     = " + str(data))
#print("verbose  = " + str(verbose))


client = carelink_client.CareLinkClient(username, password, country)
if verbose:
   print("Client created!")

if client.login():
   for i in range(repeat):
      if verbose:
         print("Starting download, count:  " + str(i+1))
      # Recent data is requested
      if(data):
         try:
            for j in range(2):
               recentData = client.getRecentData()
               # Auth error
               if client.getLastResponseCode() == 403:
                  print("GetRecentData login error (response code 403). Trying again in 1 sec!")
                  time.sleep(1)
               # Get success
               elif client.getLastResponseCode() == 200:
                  # Data OK
                  if client.getLastDataSuccess():
                     if plotter:
                        graphdata(recentData)
                     else:
                        if writeJson(recentData, "data"):
                           if verbose:
                              print("data saved!")
                  # Data error
                  else:
                     print("Data exception: " + "no details available" if client.getLastErrorMessage() == None else client.getLastErrorMessage())
                  # STOP!!!
                  break
               else:
                  print("Error, response code: " + str(client.getLastResponseCode()) + " Trying again in 1 sec!")
                  time.sleep(1)
         except Exception as e:
            print(e)

         if i < repeat - 1:
            if verbose:
               print("Waiting " + str(wait) + " minutes before next download!")
            time.sleep(wait * 60)
else:
   print("Client login error! Response code: " + str(client.getLastResponseCode()) + " Error message: " + str(client.getLastErrorMessage()))

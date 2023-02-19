#!/usr/bin/python

# Just seeing if we can graph the last 24 horus of data easily
# We will do it with a JSON first

import json
# import termplotlib as tpl
# import plotext as plt
from asciichartpy import plot
import asciichartpy
import os

# Opening JSON file
f = open('data-20211109_234101.json',)

# returns JSON object as
# a dictionary
data = json.load(f)

# We can close the file now
f.close()

# print(data['sgs'])

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
  color_list = [asciichartpy.green, asciichartpy.lightmagenta, asciichartpy.red, asciichartpy.lightblue, asciichartpy.lightred]

  # Clear and print every time we get a value
  os.system('cls' if os.name == 'nt' else 'clear')
  # print(plot(last_day_values, {'height':15, 'colors': color_list, 'min': 35, 'max': 200}))

# Print the graph at the end (faster)
print(plot(last_day_values, {'height':15, 'colors': color_list, 'min': 35}))

# Print some more useful info that we want:
# Get hours with floor division
# hours = data['timeToNextCalibrationMinutes'] // 60
# # Get additional minutes with modulus
# minutes = data['timeToNextCalibrationMinutes'] % 60

# print('\n####################################################')
# print('BG Info:')
# print('  Last Value: %i' % (data['lastSG']['sg']))
# print('    Recorded at: %s' % (data['lastSG']['datetime']))
# print('  Time In Range (24 hours): %i %%' % (data['timeInRange']))
# print('Sensor Info:')
# print('  Status: %s' % (data['calibStatus']))
# print('  Time to Next Calibration: %d h and %d min' % (hours, minutes))
# print('  Battery Percentage: %i %%' % (data['gstBatteryLevel']))
# print('Pump Info:')
# print('  Battery Percentage: %i %%' % (data['medicalDeviceBatteryLevelPercent']))
# print('  Approx Remaining Units of Insulin: %f u' %(data['reservoirRemainingUnits']))
# print('####################################################')

# Plot it!
# print(plot(last_day_values, {'height':15}))
# plt.plot(x, last_day_values)
# plt.canvas_color('black')
# plt.colorless
# plt.show()
# fig = tpl.figure()
# fig.plot(x, last_day_values, width=170, height=20)
# fig.show()

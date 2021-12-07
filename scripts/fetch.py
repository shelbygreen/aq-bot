"""
input: time of post (AM or PM)
output: aqi
"""

# import libraries
import pandas as pd
import requests
import json
from datetime import date

# get today's date
day = date.today().day
month = date.today().month
year = date.today().year

# get post time
post_time = input("Enter the time you want to post the bot: 8 or 15 ")
post_time_2 = int(post_time) + 1

# pull data from AirNow
r = requests.get('https://www.airnowapi.org/aq/data/?startDate={year}-{month}-{day}T{time1}&endDate={year}-{month}-{day}T{time2}&parameters=PM25&BBOX=-84.500651,30.275370,-84.080424,30.684863&dataType=B&format=application/json&verbose=1&monitorType=2&includerawconcentrations=0&API_KEY=2BB44069-F9EF-4CA7-8B67-C9832B168B60'.format(day = day, month = month, year = year, time1 = post_time, time2 = post_time_2)).json()

# store in dataframe
df = pd.DataFrame.from_dict(r)

# clean data
df['date'] = df['UTC'].str.split('T').str[0]
df['time'] = df['UTC'].str.split('T').str[1]

df = df.drop(['UTC'], axis=1)

df['Category'] = df['Category'].astype(str)

# create dataframe for AQI status, color, and message
conditions = pd.DataFrame({
    'category': ['1', '2', '3', '4', '5', '6'],
    'status': ['good', 'moderate', 'unhealthy for sensitive groups', 'unhealthy', 'very unhealthy', 'hazardous'],
    'color': ['green', 'yellow', 'orange', 'red', 'purple', 'maroon'],
    'message': ['In the Tallahassee area, the air quality is "good". Enjoy your outdoor activities!', 
            'In the Tallahassee area, the air quality is "moderate". If you are sensitive to air pollution, limit your time outdoors or wear a mask.',
            'In the Tallahassee area, the air quality is "unhealthy for sensitive groups',
            'In the Tallahassee area, the air quality is "unhealthy".',
            'In the Tallahassee area, the air quality is "very unhealthy',
            'In the Tallahassee area, the air quality is "hazardous.']
})

#  print status
print("the AQI for {},{}:00 is {}, category {}".format(date.today(), post_time, df.iloc[0]['AQI'], df.iloc[0]['Category']))
print("the msg is: {}".format(conditions[conditions['category'] == df.iloc[0]['Category']].iloc[0]['message']))
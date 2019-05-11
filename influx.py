#!/usr/bin/python3
import sys

import Adafruit_DHT
import datetime as dateAndTime
import time as Time
import sys
import uuid
from influxdb import InfluxDBClient
import argparse

Port = 8086
hostname = '192.168.1.189'

#Port = 27002
#hostname = 'influx-9bc11dd-girish-5108.aivencloud.com'
#usrName = 'avnadmin'
#passwd = 'oyiq1cctd5fazls1'
database = 'defaultdb'
def ConnectToInflux() :

    client = InfluxDBClient(host= hostname,
                        port=Port,
                        username='girish',
                        password='gks3050',
                        ssl=False,
                        verify_ssl=False)

    #client = InfluxDBClient(host= hostname,
    #                    port=Port,
    #                    username=usrName,
    #                    password=passwd,
    #                    ssl=True,
    #                    verify_ssl=True)
    return client



if  __name__  == "__main__":


   InflexClient = ConnectToInflux()
   print(InflexClient.get_list_database())
   print("Hello")
   InflexClient.switch_database(database)
   lowestTemp = 100
   highestTemp = 0
   lowestHumidity = 100
   highestHumidity = 0

   highTempTime = " "
   lowTempTime = " "

   highHumidityTime = " "
   lowHumidityTime = " "
   epoc = dateAndTime.datetime.now()
   todayDate = epoc.strftime("%d")
   fileName = epoc.strftime("%d-%b-%Y") + ".log"
   currentHour = epoc.strftime("%H")
   maxLogFile = epoc.strftime("%d-%b-%Y") + '_max_' + '.log'

   dateANDTime = dateAndTime.datetime.now()
   dateAndTimeString =  dateANDTime.isoformat("T") + "Z"

   json_body = [{
                  "measurement": "ClimateEvents",
                  "tags": {
                            "event": "periodic",
                            "SensorId": "00001",
                          },
                  "time"       : dateAndTimeString,
                  "fields": {
                           "Temperature" : 30.32,
                           "Humidity" : 49.34
                          }
                }]

   result   = InflexClient.write_points(json_body)

   print(result)

   while True:
      humidity, temperature = Adafruit_DHT.read_retry(11, 4)
      epoc = dateAndTime.datetime.now()
      date = epoc.strftime("%d-%b-%Y")
      time = epoc.strftime("%H:%M:%S")
     currentDate = epoc.strftime("%d")
      Hour = epoc.strftime("%H")

      if temperature > highestTemp :
         highestTemp = temperature
         highTempTime = date + ":" + time
      if temperature < lowestTemp :
         lowestTemp = temperature
         lowTempTime = date + ":" + time

      if humidity > highestHumidity:
         highestHumidity = humidity
         highHumidityTime = date + ":" + time
      if humidity < lowestHumidity:
         lowestHumidity = humidity
         lowHumidityTime = date + ":" + time

      #print epoc.strftime("%d-%b-%Y")
      #print epoc.strftime("%H:%M:%S")
      #print temperature, humidity


      if currentHour != Hour:
         print ("Change of hour detected")
         maxlog = open(maxLogFile,'a')
         buf = "Max Temp:" + " " + str(highestTemp) + " , " + str(highTempTime)
         maxlog.write(buf)
         maxlog.write("\n")
         buf = "Min Temp:" + " " + str(lowestTemp) + " , " + str(lowTempTime)
         maxlog.write(buf)
         maxlog.write("\n")
         buf = "Max Humidity:" + " " + str(highestHumidity) + " , " + str(highHumidityTime)
         maxlog.write(buf)
         maxlog.write("\n")
         buf = "Min Humidity:" + " " + str(lowestHumidity) +" , " + str(lowHumidityTime)
         maxlog.write(buf)
         maxlog.write("\n")
         maxlog.close()
         currentHour = Hour
         data = { 'Max Temp'     : str(highestTemp),
                  'Min Temp'     : str(lowestTemp),
                  'Max Humidity' : str(highestHumidity),
                  'Min Humidity' : str(lowestHumidity)
               }
         #WriteToInflex()
         #success = deviceCli.publishEvent("MaxMin", "json", data, qos=0, on_publish=myOnPublishCallback)
         #if not success:
         #       print("Not connected to IoTF")



      if currentDate != todayDate:
         # Date changed so record max and min details
         log = open(fileName,'a')
         buf = "Max Temp:" + " " + str(highestTemp) + " , " + str(highTempTime)
         log.write(buf)
         log.write("\n")
         buf = "Min Temp:" + " " + str(lowestTemp) + " , " + str(lowTempTime)
         log.write(buf)
         log.write("\n")
         buf = "Max Humidity:" + " " + str(highestHumidity) + " , " + str(highHumidityTime)
         log.write(buf)
         log.write("\n")
         buf = "Min Humidity:" + " " + str(lowestHumidity) +" , " + str(lowHumidityTime)
         log.write(buf)
         log.write("\n")
         log.close()
         todayDate = currentDate
         fileName = epoc.strftime("%d-%b-%Y") + ".log"
         maxLogFile = epoc.strftime("%d-%b-%Y") + '_max_' + '.log'

      log = open(fileName,'a')
      buf = str(epoc) + " , " +  dateAndTimeString + " , " + date + " , " + time + " , " + str(temperature) + " , " + str(humidity)
      data = {
                'Time' : time,
                'Temp' : str(temperature),
                'Humidity': str(humidity)
             }

      dateANDTime = dateAndTime.datetime.now()
      dateAndTimeString =  dateANDTime.isoformat("T") + "Z"
      #print(dateAndTimeString)
      json_body = [{
                  "measurement": "ClimateEvents",
                  "tags": {
                            "event": "periodic",
                          },
                  "fields": {
                           "Temperature" : temperature,
                           "Humidity" : humidity
                          }
                }]
      #json_body = [{
      #            "measurement": "ClimateEvents",
      #            "tags": {
      #                      "event": "periodic",
      #                      "SensorId": "00001",
      #                    },
      #            "time"       : dateAndTimeString,
      #            "fields": {
      #                     "Temperature" : temperature,
      #                     "Humidity" : humidity
      #                    }
      #          }]

      #json_body = [{
      #            "measurement": "ClimateEvents",
      #            "time"       : dateAndTimeString,
      #            "fields": {
      #                     "Temperature" : temperature,
      #                     "Humidity" : humidity
      #                    }
      #          }]
      #print(json_body)
      result   = InflexClient.write_points(json_body)
      #print(result)

      log.write(buf)
      log.write("\n")
      log.close()
      # Working one
      #results = InflexClient.query('SELECT "Temperature" FROM "defaultdb"."autogen"."ClimateEvents"')
      #print(results.raw)

      #Time.sleep(60*5) #Sleep for 5  minute
      Time.sleep(30) #Sleep for 5  minute


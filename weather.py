#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import urllib2
import csv
import json
import time
import bottoken

def getWeather():
    return [getAirCondition()[0], getWaterTemp(0), "%.1f" % getAirCondition()[1], getAirCondition()[2], getForecast()]

def getWaterTempVal():
    #Url with the table(csv) of temperatures from enz in bessigheim
    url = "https://www.lubw.baden-wuerttemberg.de/servlet/is/84696/data.csv"
    try:
        #Try reading the values from the url
        response = urllib2.urlopen(url)
        spamreader = csv.reader(response, delimiter=';', quotechar='|')
        #Get rid of description from the csv
        spamreader.next()
        #Get the actual values
        tmp = spamreader.next()
        #Parse the values from the table content
        time = int(tmp[0].split(' ')[1].split(":")[0]) + 1
        temp = float(".".join(tmp[1].split(",")))

        return [temp, time]
    except:
        return -1

def getAirCondition():
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather/?id=2949012&lang=de&units=metric&APPID=' + bottoken.weatherApiKey
        response = urllib2.urlopen(url);
        data = json.loads(response.read())
        wTime = time.strftime("%H:%M", time.gmtime(data.get('dt', '')))
        wDesc = str(data.get('weather', '')[0].get('description', '').encode('utf-8'))
        wTemp = data.get('main', '').get('temp', '')
        wIcon = str(data.get('weather', '')[0].get('icon', ''))[:-1]


        return (wTime, wTemp, wIcon, wDesc)
        #return 'Das Wetter um ' + wTime + ': ' + str(data.get('weather', '')[0].get('description', '').encode('utf-8')) + ' bei ' + str(data.get('main', '').get('temp', '')) + '°C\n\n' + getWeatherForecast()
    except:
        return 0
        #return 'Momentan ist keine Wetterabfrage verfügbar. Versuch es später noch einmal.'

def getWaterTemp(choice):
    #Getting the actual temperature
    actl = getWaterTempVal()

    if actl == -1:
        return 'Momentan steht keine Wassertemperatur zur Verfügung. Versuch es später noch einmal.'
    else:
        time = actl[1]

        msg = 'Zwischen ' + str(time) + '-' + str(time + 1) + 'Uhr betrug die Wassertemperatur: '
        if choice == 0:
            return str(actl[0])
            #return msg + str(actl[0]) + '°C'
        elif choice == 1:
            return msg + convertTempToMen(actl[0]) + 'cm'


def getForecast():
    try:
        url = 'http://api.openweathermap.org/data/2.5/forecast?id=2949012&lang=de&units=metric&APPID=' + bottoken.weatherApiKey
        response = urllib2.urlopen(url);
        data = json.loads(response.read())
        fcData = []
        fStr = ''

        for i in range(1,4):
            fStr += 'Wettervorhersage für '
            #fStr += time.strftime("%H:%M", time.gmtime(data.get('list', '')[0]))
            fStr += time.strftime("%H:%M", time.gmtime(data.get('list', '')[i].get('dt', '')))
            fStr += ': '
            fStr += str(data.get('list', '')[i].get('weather')[0].get('description', '').encode('utf-8'))
            fStr += ' bei '
            fStr += str(data.get('list', '')[i].get('main').get('temp', ''))
            fStr += '°C\n'
            fcData.append([time.strftime("%H:%M", time.gmtime(data.get('list', '')[i].get('dt', ''))), "%.1f" % data.get('list', '')[i].get('main').get('temp', ''), str(data.get('list', '')[i].get('weather')[0].get('icon', '').encode('utf-8'))[:-1]])
        print fStr
        print fcData

        return fcData 
        #return fStr
    except Exception, err:
        print ('ERROR: %s\n' % str(err))
        return 'Eine Wettervorhersage ist momentan nicht möglich.'
    #except:
    #    return 'Eine Wettervorhersage ist momentan nicht möglich.'

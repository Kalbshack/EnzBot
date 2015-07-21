#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''Simple Bot to reply Telegram messages'''

import telegram
import csv
import time
import urllib2
import bottoken
import json
import time

# Telegram Bot Authorization Token
bot = telegram.Bot(token=bottoken.defaultbot)

# This will be our global variable to keep the latest update_id when requesting
# for updates. It starts with the latest update_id if available.
try:
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
except IndexError:
    LAST_UPDATE_ID = None


def readCommand():
    global LAST_UPDATE_ID

    # Request updates from last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            command = update.message.text.lower()

            if (command):
                if command == "/temp":
                    bot.sendMessage(chat_id=chat_id, text=wTemp(0) + '\n' + getWeather())
                elif command == "/mentemp":
                    bot.sendMessage(chat_id=chat_id, text=wTemp(1) + '\n' + getWeather())
                elif command == "/weather":
                    getWeather()
                elif command == "/help" or command == "/start":
                    bot.sendMessage(chat_id=chat_id, text=info())
                else:
                    bot.sendMessage(chat_id=chat_id, text="Failure is simply the opportunity to begin again, this time more intelligently.")

                # Updates global offset to get the new updates
                LAST_UPDATE_ID = update.update_id

def wTemp(choice):
    #Getting the actual temperature
    actl = getValues()

    if actl[0] == -10.0 and actl[1] == -1:
        return 'Momentan steht keine Temperatur zur Verfügung. Versuch es später noch einmal.'
    else:
        time = actl[1]

        msg = 'Zwischen ' + str(time) + '-' + str(time + 1) + 'Uhr betrug die Wassertemperatur: '
        if choice == 0:
            return msg + str(actl[0]) + '°C'
        elif choice == 1:
            return msg + convertTempToMen(actl[0]) + 'cm'

def getWeather():
    url = 'http://api.openweathermap.org/data/2.5/weather/?id=2949012&lang=de&units=metric&APPID=' + bottoken.weatherApiKey
    response = urllib2.urlopen(url);
    data = json.loads(response.read())
    wTime = time.strftime("%H:%M", time.gmtime(data.get('dt', '')))
    return 'Das Wetter um ' + wTime + ': ' + str(data.get('weather', '')[0].get('description', '')) + ' bei ' + str(data.get('main', '').get('temp', '')) + '°C\n\n' + getWeatherForecast()

def getWeatherForecast():
    url = 'http://api.openweathermap.org/data/2.5/forecast?id=2949012&lang=de&units=metric&APPID=' + bottoken.weatherApiKey
    response = urllib2.urlopen(url);
    data = json.loads(response.read())

    fStr = ''

    for i in range(2):
        fStr += 'Wettervorhersage für '
        #fStr += time.strftime("%H:%M", time.gmtime(data.get('list', '')[0]))
        fStr += time.strftime("%H:%M", time.gmtime(data.get('list', '')[i].get('dt', '')))
        fStr += ': '
        fStr += str(data.get('list', '')[i].get('weather')[0].get('description', ''))
        fStr += ' bei '
        fStr += str(data.get('list', '')[i].get('main').get('temp', ''))
        fStr += '°C\n'


    return fStr


def getValues():
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
    except urllib2.URLError:
        return [-10.0, -1]


def info():
    #Info which is displayed by typing /help or starting the Bot
    return 'Hi, ich bin der @EnzBot.\nDu hast momentan folgende Möglichkeiten:\n\n/temp Zeigt die Wassertemperatur\n/mentemp Zeigt die Wassertemperatur für Männer\n/help Zeigt diese Info an'

def convertTempToMen(val):
    #Converting the temperature(in) according to the average penis size(out) of the german (8,6cm)

    inMin = 10.0
    inMax = 25.0
    outMin = 1.0
    outMax = 8.6

    if val < inMin: val = inMin

    newVal = (val - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    return "%.2f" % newVal


if __name__ == '__main__':
    while True:
        readCommand()
        time.sleep(3)

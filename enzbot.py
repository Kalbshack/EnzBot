#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''Simple Bot to reply Telegram messages'''

import telegram
import time
import bottoken
import image
import weather

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

            if update.message.text:
                print "You got text"

                command = update.message.text.lower()
                if (command):
                    if command == "/temp":
                        image.makeImage(weather.getWeather())
                        bot.sendPhoto(chat_id=chat_id, photo='http://kalbshack.net/test.png')
                    elif command == "/img":
                        image.makeImage(weather.getWeather())
                        bot.sendPhoto(chat_id=chat_id, photo='http://kalbshack.net/test.png')
                    #elif command == "/mentemp":
                        #bot.sendMessage(chat_id=chat_id, text=wTemp(1) + '\n' + getWeather())
                        #print "mentemp"
                    #elif command == "/weather":
                        #bot.sendMessage(chat_id=chat_id, text=getWeather())
                    elif command == "/help" or command == "/start":
                        bot.sendMessage(chat_id=chat_id, text=info())
                    else:
                        bot.sendMessage(chat_id=chat_id, text="Failure is simply the opportunity to begin again, this time more intelligently.")
            else:
                print "No command found"
                bot.sendMessage(chat_id=chat_id, text="Failure is simply the opportunity to begin again, this time more intelligently.")

            # Updates global offset to get the new updates
            LAST_UPDATE_ID = update.update_id

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

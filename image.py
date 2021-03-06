#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os.path

path = os.path.dirname(os.path.realpath(__file__))
#Different type/sizes of fonts
title = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",30)
semititle = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",25)
cright = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",10)
main = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",15)

def makeImage(weather):
    time = weather[0]
    wTemp = weather[1]
    aTemp = weather[2]
    icon = weather[3]
    forecast = weather[4]
    #Get the weather symbol
    miniIconSize = 25
    icn = Image.open(path + '/icons/' + icon + '.png')
    icn.thumbnail((80, 80), Image.ANTIALIAS)

    aTempIcon = Image.open(path + '/icons/aTemp.png')
    wTempIcon = Image.open(path + '/icons/wTemp.png')
    wTempIcon.thumbnail((25,25), Image.ANTIALIAS)

    forIcon = []
    forIcon.append(Image.open(path + '/icons/' + forecast[0][2] + '.png'))
    forIcon[0].thumbnail((miniIconSize, miniIconSize), Image.ANTIALIAS)
    forIcon.append(Image.open(path + '/icons/' + forecast[1][2] + '.png'))
    forIcon[1].thumbnail((miniIconSize, miniIconSize), Image.ANTIALIAS)
    forIcon.append(Image.open(path + '/icons/' + forecast[2][2] + '.png'))
    forIcon[2].thumbnail((miniIconSize, miniIconSize), Image.ANTIALIAS)

    white = Image.new("RGBA", (80,80),(255,255,255))
    forWhite = Image.new("RGBA", (miniIconSize,miniIconSize),(255,255,255))
    degSign = '°'.decode('utf-8')

    #img = Image.new("RGBA", (300,150),(14,93,138))
    img = Image.open(path + '/bg.jpeg')
    img.paste(white, (210,5), icn)
    draw = ImageDraw.Draw(img)

    #Creating Head
    draw.text((5, 5),('Enz ' + time),(255,255,255),font=title)
    #Creating air temperature incl. Icon
    draw.text((218, 90),str(aTemp) + degSign,(255,255,255),font=title)
    img.paste(aTempIcon, (200, 80), aTempIcon)
    #Creating water temperature incl. Icon
    draw.text((230, 120),str(wTemp) + degSign,(255,255,255),font=semititle)
    img.paste(wTempIcon, (200, 124), wTempIcon)
    #Creating forecast temperature incl. Icon
    draw.text((5, 65),forecast[0][0] + "          " + str(forecast[0][1]) + degSign,(255,255,255),font=main)
    img.paste(forWhite, (65,60), forIcon[0])
    draw.text((5, 95),forecast[1][0] + "          " + str(forecast[1][1]) + degSign,(255,255,255),font=main)
    img.paste(forWhite, (65,90), forIcon[1])
    draw.text((5, 125),forecast[2][0] + "          " + str(forecast[2][1]) + degSign,(255,255,255),font=main)
    img.paste(forWhite, (65,120), forIcon[2])

    draw = ImageDraw.Draw(img)
    #img.save("test.png")
    img.save("/home/lars/web/test.png")

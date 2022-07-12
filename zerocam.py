#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*****************************************************************************
#
# This is the "zerocam" script.
#
# Module        : main module, zcam.py
# Author        : Swen Hopfe (dj)
# Design        : 2018-01-16
# Last modified : 2019-09-14
#
# The python script works on Raspberry Pi 2/3/B/+
# with PiCam, TFT display and keyboard and was tested on a Pi Zero W.
#
# Take pictures or infrared pics with your mobile zerocam...
#
#*****************************************************************************

minlcd = False   # kleines LCD auf Minivariante vorhanden
abertc = False   # Echtzeituhr vorhanden
tastmode = True  # Tastaturmode True = Gehaeusetaster auf Minivariante inaktiv

import time
import sys
import os
import ftplib
import RPi.GPIO as GPIO
import subprocess
import time
import signal
import datetime
from random import randint
from picamera import PiCamera

#-----------------------------------------------------------------------------

ge = True
if os.environ.get('DISPLAY','') == '':
     ge = False
else:
     from Tkinter import *
from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageTk

if abertc:
   from ABE_RTCPi import RTC
   from ABE_helpers import ABEHelpers
if minlcd:
   import LCD_1in44
   import LCD_Config

#-----------------------------------------------------------------------------

imgpath = "/home/pi/scripts/thumbs/pre.gif"

#-----------------------------------------------------------------------------

KEY_UP_PIN     = 6
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)

#-----------------------------------------------------------------------------

iso = 0  # automatic
ips = False # Infrarot-Preset

#-----------------------------------------------------------------------------

def press_i(event):
    global iso
    global ge
    global ips

    #----------------------------------
    # Infrarot Preset

    ips = True

    #----------------------------------

    if(ge):
       txt.insert(END,"Voreinstellung für Infrarot.\n")
       txt.see(END)
    print "Voreinstellung für Infrarot."
    print "----------------------------------------------------------"

#-----------------------------------------------------------------------------

def press_n(event):
    global iso
    global ge
    global ips

    #----------------------------------
    # Standard Preset

    iso = 0
    ips = False

    #----------------------------------

    if(ge):
       txt.insert(END,"Standardeinstellung.\n")
       txt.see(END)
    print "Standardeinstellung gesetzt."
    print "----------------------------------------------------------"

#-----------------------------------------------------------------------------

def press_num0(event):
    global iso
    global ge
    iso = 0
    if(ge):
       txt.insert(END,"ISO Automatik.\n")
       txt.see(END)
    print "ISO auf Automatik gesetzt."
    print "----------------------------------------------------------"

def press_num1(event):
    global iso
    global ge
    iso = 100
    if(ge):
       txt.insert(END,"ISO auf 100 gesetzt.\n")
       txt.see(END)
    print "ISO auf 100 gesetzt."
    print "----------------------------------------------------------"

def press_num2(event):
    global iso
    global ge
    iso = 200
    if(ge):
       txt.insert(END,"ISO auf 200 gesetzt.\n")
       txt.see(END)
    print "ISO auf 200 gesetzt."
    print "----------------------------------------------------------"

def press_num3(event):
    global iso
    global ge
    iso = 300
    if(ge):
       txt.insert(END,"ISO auf 300 gesetzt.\n")
       txt.see(END)
    print "ISO auf 300 gesetzt."
    print "----------------------------------------------------------"

def press_num4(event):
    global iso
    global ge
    iso = 400
    if(ge):
       txt.insert(END,"ISO auf 400 gesetzt.\n")
       txt.see(END)
    print "ISO auf 400 gesetzt."
    print "----------------------------------------------------------"

def press_num5(event):
    global iso
    global ge
    iso = 500
    if(ge):
       txt.insert(END,"ISO auf 500 gesetzt.\n")
       txt.see(END)
    print "ISO auf 500 gesetzt."
    print "----------------------------------------------------------"

def press_num6(event):
    global iso
    global ge
    iso = 600
    if(ge):
       txt.insert(END,"ISO auf 600 gesetzt.\n")
       txt.see(END)
    print "ISO auf 600 gesetzt."
    print "----------------------------------------------------------"

def press_num7(event):
    global iso
    global ge
    iso = 700
    if(ge):
       txt.insert(END,"ISO auf 700 gesetzt.\n")
       txt.see(END)
    print "ISO auf 700 gesetzt."
    print "----------------------------------------------------------"

def press_num8(event):
    global iso
    global ge
    iso = 800
    if(ge):
       txt.insert(END,"ISO auf 800 gesetzt.\n")
       txt.see(END)
    print "ISO auf 800 gesetzt."
    print "----------------------------------------------------------"

#-----------------------------------------------------------------------------

def press_u(event):
    clicked8()

def clicked8():
   print "Probiere FTP..."
   global ge
   if(ge):
      txt.insert(END,"Probiere FTP...\n")
      txt.see(END)
   if minlcd:
      image = Image.open('/home/pi/scripts/thumbs/p07.bmp')
      LCD.LCD_ShowImage(image.rotate(180),0,0)

   time.sleep(2)
   try:
     ftp = ftplib.FTP('hosting111801.a2f33.netcup.net', 'statcam', 'sw371146_AS')#
   except:
     print "...Kein FTP möglich."
     print "----------------------------------------------------------"
     if(ge):
        txt.insert(END,"...kein FTP möglich.\n")
        txt.see(END)
   else:
     print "Starte FTP-Übertragung..."
     if(ge):
        txt.insert(END,"Starte FTP-Übertragung...\n")
        txt.see(END)
     files = os.listdir(outpath)
     for f in files:
         fi =  open(f,"r")
         ftp.storbinary("STOR " + f, fi)
         fi.close
     print "...fertig."
     print "----------------------------------------------------------"
     if(ge):
        txt.insert(END,"...fertig.\n")
        txt.see(END)
   ftp.quit
   if minlcd:
      image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
      LCD.LCD_ShowImage(image.rotate(180),0,0)

   #print "Kopiere Files ins Archiv..."
   #time.sleep(2)
   #os.system("bash -c \"sudo cp \" + outpath + \"/*.jpg /home/pi/scripts/archive/\"")
   #print "...fertig."

#-----------------------------------------------------------------------------

def press_f(event):
    clicked6()

def clicked6():
    global outpath
    print "Formatiere..."
    global ge
    if(ge):
       txt.insert(END,"Formatiere...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p05.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

    time.sleep(2)
    os.system("bash -c \"sudo rm -r -f /home/pi/scripts/images/\"")
    time.sleep(3)
    os.mkdir("/home/pi/scripts/images")
    os.mkdir(outpath)
    os.chdir(outpath)
    print "...fertig."
    print "----------------------------------------------------------"
    if(ge):
       txt.insert(END,"...fertig.\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

#-----------------------------------------------------------------------------

def press_l(event):
    clicked5()

def clicked5():
    global sr
    global ge
    print "Lösche Files in " + sr + "..."
    if(ge):
       txt.insert(END,"Lösche Files in " + sr + "...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p04.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

    time.sleep(2)
    os.system("bash -c \"sudo rm *.jpg\"")
    print "...fertig."
    print "----------------------------------------------------------"
    if(ge):
       txt.insert(END,"...fertig.\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

#-----------------------------------------------------------------------------

def press_v(event):
    clicked1()

def clicked1():
    global ge
    global lbl2
    global btn9
    global iso
    global brn
    global ips

    print "Erstelle Vorschau..."
    if(ge):
       txt.insert(END,"Erstelle Vorschau...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p03.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)


    if ips:
       subprocess.call(["/home/pi/scripts/vorschau_inf.sh"])
    else:
       if   iso == 0:   isostr = "auto"
       elif iso == 100: isostr = "100"
       elif iso == 200: isostr = "200"
       elif iso == 300: isostr = "300"
       elif iso == 400: isostr = "400"
       elif iso == 500: isostr = "500"
       elif iso == 600: isostr = "600"
       elif iso == 700: isostr = "700"
       elif iso == 800: isostr = "800"
       subprocess.call(["/home/pi/scripts/vorschau_nrm.sh","/home/pi/scripts/vorschau.jpg",isostr])


    path = "/home/pi/scripts/vorschau.jpg"
    print "...fertig."
    print "----------------------------------------------------------"
    if(ge):
       txt.insert(END,"...fertig.\n")
       txt.see(END)

       size = 480, 360
       newpath = "/home/pi/scripts/vorschau.gif"
       im = Image.open("/home/pi/scripts/vorschau.jpg")
       im.thumbnail(size)
       im.save(newpath)

       img_b = Image.open(newpath)
       img_c = img_b.resize((400, 300))
       img_a = ImageTk.PhotoImage(img_c)
       lbl2 = Label(master = frm, image = img_a, font=("Helvetica", 10, "bold"))
       lbl2.image = img_a
       lbl2.place(x=40, y=10, width=400, height=300)

       btn9 = Button(master = frm, text="Zurück", font=("Helvetica", 11, "bold"), command=clicked9)
       btn9.place(x=300, y=270, width=80, height=30)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

#-----------------------------------------------------------------------------

def press_z(event):
    clicked9()

def clicked9():
    lbl2.destroy()
    btn9.destroy()

#-----------------------------------------------------------------------------

def press_s(event):
    clicked2()

def clicked2():
    print "Fahre Kamera herunter..."
    print "----------------------------------------------------------"
    global ge
    if(ge):
       txt.insert(END,"Fahre Kamera herunter...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p99.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)
       LCD_Config.Driver_Delay_ms(1000)
    counts(5)

def counts(count):
    global ge
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p98.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)
    if(ge):
       if count > 0:
           btn2["text"] = count
           frm.after(1000, counts, count -1)
       elif count == 0:
           subprocess.call(["sudo","shutdown","now"])
    else:
       time.sleep(count)
       subprocess.call(["sudo","shutdown","now"])

#-----------------------------------------------------------------------------

def press_r(event):
    print "Rebooting..."
    print "----------------------------------------------------------"
    time.sleep(5)
    subprocess.call(["sudo","reboot"])

#-----------------------------------------------------------------------------

def press_a(event):
    clicked3()

def clicked3():
    global ge
    global lbl2
    global btn9
    global iso
    global brn
    global ips

    print "Nehme Bild auf..."
    if(ge):
       txt.insert(END,"Nehme Bild auf...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p01.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

    br = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)) + ".jpg"

    if ips:
       subprocess.call(["/home/pi/scripts/capture_inf.sh",br])
    else:
       if   iso == 0:   isostr = "auto"
       elif iso == 100: isostr = "100"
       elif iso == 200: isostr = "200"
       elif iso == 300: isostr = "300"
       elif iso == 400: isostr = "400"
       elif iso == 500: isostr = "500"
       elif iso == 600: isostr = "600"
       elif iso == 700: isostr = "700"
       elif iso == 800: isostr = "800"
       subprocess.call(["/home/pi/scripts/capture_nrm.sh",br,isostr])

    print "...fertig."
    print "----------------------------------------------------------"
    if(ge):
       txt.insert(END,"...fertig.\n")
       txt.see(END)

       size = 480, 360
       newpath = "/home/pi/scripts/vorschau.gif"
       im = Image.open(br)
       im.thumbnail(size)
       im.save(newpath)

       img_b = Image.open(newpath)
       img_c = img_b.resize((400, 300))
       img_a = ImageTk.PhotoImage(img_c)
       lbl2 = Label(master = frm, image = img_a, font=("Helvetica", 10, "bold"))
       lbl2.image = img_a
       lbl2.place(x=40, y=10, width=400, height=300)

       btn9 = Button(master = frm, text="Zurück", font=("Helvetica", 11, "bold"), command=clicked9)
       btn9.place(x=300, y=270, width=80, height=30)

    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

    # dname = "zc" + rtc.read_date() + ".jpg"
    # subprocess.call(["sudo","raspistill","-h","1800","-w","2400","-rot","180","-t","100","-q","90","-o",dname])
    # subprocess.call(["sudo","raspistill","-rot","180","-t","100","-q","92","-o",dname])

#-----------------------------------------------------------------------------

def press_t(event):
    clicked4()

def clicked4():
    global ge
    print "Nehme Bild auf nach 10s..."
    if(ge):
       txt.insert(END,"Nehme Bild auf nach 10s...\n")
       txt.see(END)
    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p02.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)
    counta(10)

def counta(count):
  global ge
  global lbl2
  global btn9
  global brn
  if(ge):
    if count > 0:
        btn6["text"] = count
        frm.after(1000, counta, count -1)
    elif count == 0:
        br = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)) + ".jpg"

        if ips:
          subprocess.call(["/home/pi/scripts/capture_inf.sh",br])
        else:
          if   iso == 0:   isostr = "auto"
          elif iso == 100: isostr = "100"
          elif iso == 200: isostr = "200"
          elif iso == 300: isostr = "300"
          elif iso == 400: isostr = "400"
          elif iso == 500: isostr = "500"
          elif iso == 600: isostr = "600"
          elif iso == 700: isostr = "700"
          elif iso == 800: isostr = "800"
          subprocess.call(["/home/pi/scripts/capture_nrm.sh",br,isostr])


        subprocess.call(["sudo","raspistill",b1str,b2str,i1str,i2str,"-rot","180","-t","100","-o",br])

        print "...fertig."
        print "----------------------------------------------------------"
        txt.insert(END,"...fertig.\n") 
        txt.see(END)
        btn6.configure(text = "verzögert")

        size = 480, 360
        newpath = "/home/pi/scripts/vorschau.gif"
        im = Image.open(br)
        im.thumbnail(size)
        im.save(newpath)

        img_b = Image.open(newpath)
        img_c = img_b.resize((400, 300))
        img_a = ImageTk.PhotoImage(img_c)
        lbl2 = Label(master = frm, image = img_a, font=("Helvetica", 10, "bold"))
        lbl2.image = img_a
        lbl2.place(x=40, y=10, width=400, height=300)

        btn9 = Button(master = frm, text="Zurück", font=("Helvetica", 11, "bold"), command=clicked9)
        btn9.place(x=300, y=270, width=80, height=30)

        # dname = "zc" + rtc.read_date() + ".jpg"
        # subprocess.call(["sudo","raspistill","-h","1800","-w","2400","-rot","180","-t","100","-q","90","-o",dname])
        # subprocess.call(["sudo","raspistill","-rot","180","-t","100","-q","92","-o",dname])
  else:
        br = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)) + ".jpg"


        if ips:
          subprocess.call(["/home/pi/scripts/capture_inf.sh",br])
        else:
          if   iso == 0:   isostr = "auto"
          elif iso == 100: isostr = "100"
          elif iso == 200: isostr = "200"
          elif iso == 300: isostr = "300"
          elif iso == 400: isostr = "400"
          elif iso == 500: isostr = "500"
          elif iso == 600: isostr = "600"
          elif iso == 700: isostr = "700"
          elif iso == 800: isostr = "800"
          subprocess.call(["/home/pi/scripts/capture_nrm.sh",br,isostr])


        print "...fertig."
        print "----------------------------------------------------------"

  if minlcd:
     image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
     LCD.LCD_ShowImage(image.rotate(180),0,0)

#-----------------------------------------------------------------------------

def press_h(event):
    clicked7()

def clicked7():
    global ge
    global tastmode

    if(ge):
       txt.insert(END,"Shortkeys: a t v s r l f u h 0-8 i n\n")
       txt.insert(END,"a  - Aufnahme\n")
       txt.insert(END,"t  - Timer, Aufnahme nach 10s\n")
       txt.insert(END,"v  - Vorschau ohne Speichern der Aufnahme\n")
       txt.insert(END,"s/r- Shutdown/Reboot Kamera\n")
       txt.insert(END,"l  - Löschen der Files im aktuellen Verzeichnis\n")
       txt.insert(END,"f  - Formatieren (Bildverzeichnisse löschen)\n")
       txt.insert(END,"u  - Upload des aktuellen Verzeichnis per FTP\n")
       txt.insert(END,"h  - Hilfe\n")
       txt.insert(END,"0  - ISO Einstellung 0(auto) bis 8(800)\n")
       txt.insert(END,"i  - Voreinstellung für Infrarot\n")
       txt.insert(END,"n  - Normale / Standardeinstellung\n")
       txt.see(END)
    else:
       if tastmode == False:
          tastmode = True
          print "Tastaturmode eingeschalten"
          print "----------------------------------------------------------"
          image = Image.open('/home/pi/scripts/thumbs/p06.bmp')
          if minlcd:
             LCD.LCD_ShowImage(image.rotate(180),0,0)
             LCD_Config.Driver_Delay_ms(1000)
       else:
          tastmode = False
          print "Tastaturmode ausgeschalten"
          print "----------------------------------------------------------"
          image = Image.open('/home/pi/scripts/thumbs/p09.bmp')
          if minlcd:
             LCD.LCD_ShowImage(image.rotate(180),0,0)
             LCD_Config.Driver_Delay_ms(1000)

    print "Shortkeys sind:"
    print "a - Aufnahme"
    print "t - Timer, Aufnahme nach 10s"
    print "v - Vorschau ohne Speichern der Aufnahme"
    print "s - Shutdown Kamera"
    print "r - Reboot Kamera"
    print "l - Löschen der Files im aktuellen Verzeichnis"
    print "f - Formatieren (Bildverzeichnisse löschen)"
    print "u - Upload des aktuellen Verzeichnis per FTP"
    print "h - Hilfe (Tastaturwechsel)"
    print "0 - ISO Einstellung 0(auto) bis 8(800)"
    print "i - Voreinstellung für Infrarot"
    print "n - Normale / Standardeinstellung"
    print "----------------------------------------------------------"

    if minlcd:
       image = Image.open('/home/pi/scripts/thumbs/p08.bmp')
       LCD.LCD_ShowImage(image.rotate(180),0,0)

#-----------------------------------------------------------------------------

def callback(e):
    img1 = PhotoImage(file=imgpath)
    lbl2.configure(image = img1)
    lbl2.image = img1

#-----------------------------------------------------------------------------

#i2c_helper = ABEHelpers()
#bus = i2c_helper.get_smbus()
#rtc = RTC(bus)

# set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS
# rtc.set_date("2018-08-25T23:40:00")

print " "
print "----------------------------------------------------------"
print "-----   zerocam R4 14.09.19                          -----"
print "----------------------------------------------------------"
print " "

if minlcd:
   LCD = LCD_1in44.LCD()
   Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
   LCD.LCD_Init(Lcd_ScanDir)
   LCD.LCD_Clear()

   image = Image.open('/home/pi/scripts/thumbs/p00.bmp')
   LCD.LCD_ShowImage(image.rotate(180),0,0)
   LCD_Config.Driver_Delay_ms(1000)

sr = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))

outpath = "/home/pi/scripts/images/" + sr
os.mkdir(outpath)
os.chdir(outpath)

print "Kamera bereit. Shortkeys sind:"
print "a - Aufnahme"
print "t - Timer, Aufnahme nach 10s"
print "v - Vorschau ohne Speichern der Aufnahme"
print "s - Shutdown Kamera"
print "r - Reboot Kamera"
print "l - Löschen der Files im aktuellen Verzeichnis"
print "f - Formatieren (Bildverzeichnisse löschen)"
print "u - Upload des aktuellen Verzeichnis per FTP"
print "h - Hilfe (Tastaturwechsel)"
print "0 - ISO Einstellung 0(auto) bis 8(800)"
print "i - Voreinstellung für Infrarot"
print "n - Normale / Standardeinstellung"
print "----------------------------------------------------------"
print "Warte auf Eingabe..."
print "----------------------------------------------------------"

if(ge):

   win = Tk()
   win.attributes("-fullscreen", True)
   win.title("zerocam 4")

   #win.geometry('480x320')
   win.geometry("%dx%d+0+0" % (480, 320))

   frm = Frame(master = win, width = 480, height = 320, bg ='grey')
   frm.pack()

   sw = 480
   sh = 320
   bb = 90
   bh = 30
   bho = 25
   bqb = 80
   bqh = 80
   ro = 15
   rl = 15
   rms = 15
   rmw = 15
   rmwr = 25
   ru = 15

   btn1 = Button(master = frm, text="Vorschau", font=("Helvetica", 11, "bold"), command=clicked1)
   btn1.place(x=sw-rl-bqb, y=ro, width=bqb, height=bqh)

   btn3 = Button(master = frm, text="Aufnahme", font=("Helvetica", 11, "bold"), command=clicked3)
   btn3.place(x=sw-rl-bqb, y=ro+bqb+rmwr, width=bqb, height=bqh)

   btn6 = Button(master = frm, text="verzögert", font=("Helvetica", 11, "bold"), command=clicked4)
   btn6.place(x=sw-rl-bqb, y=ro+bqb+rmwr+bqb+rmwr, width=bqb, height=bqh)


   btn4 = Button(master = frm, text="Löschen", font=("Helvetica", 11, "bold"), command=clicked5)
   btn4.place(x=rl, y=sh-ru-bh, width=bb, height=bh)

   btn5 = Button(master = frm, text="Formatieren", font=("Helvetica", 11, "bold"), command=clicked6)
   btn5.place(x=rl+bb+rms, y=sh-ru-bh, width=bb+10, height=bh)

   btn8 = Button(master = frm, text="Upload", font=("Helvetica", 11, "bold"), command=clicked8)
   btn8.place(x=rl+bb+rms+bb+25+rms, y=sh-ru-bh, width=bb, height=bh)

   txt = Text(master = frm, wrap='word', width=45, height=5, bg='beige', font=("Mono", 9, "bold"))
   scroll = Scrollbar(master = frm)
   scroll.config(command = txt.yview)
   txt.config(yscrollcommand = scroll.set)
   txt.place(x=rl, y=ro+bh+rmw, width=sw-rl-rl-rms-bqb, height=sh-ro-ru-rmw-rmw-bh-bh)
   scroll.place(x=sw-rl-10-rms-bqb, y=ro+bh+rmw, width=10, height=sh-ro-ru-rmw-rmw-bh-bh)

   lbl1 = Label(master = frm, text = sr, font=("Helvetica", 10, "bold"))
   lbl1.place(x=rl, y=ro, width=bb, height=20)

   btn2 = Button(master = frm, text="Shutdown", font=("Helvetica", 11, "bold"), command=clicked2)
   btn2.place(x=rl+bb+rms+10, y=ro, width=bb, height=bho)

   btn7 = Button(master = frm, text="Hilfe", font=("Helvetica", 11, "bold"), command=clicked7)
   btn7.place(x=rl+bb+rms+bb+rms+20, y=ro, width=bb, height=bho)

   #img_b = Image.open(imgpath)
   #img_c = img_b.resize((400, 300))
   #img_a = ImageTk.PhotoImage(img_c)
   #lbl2 = Label(master = frm, image = img_a, font=("Helvetica", 10, "bold"))
   #lbl2.image = img_a
   #lbl2.place(x=rl, y=ro, width=400, height=300)

   #txt.insert(END,rtc.read_date()+"\n")
   txt.insert(END,"Kamera bereit.\n")
   txt.insert(END,"Shortkeys: a t v s r l f u h 0-8 i n\n")
   txt.insert(END,"a  - Aufnahme\n")
   txt.insert(END,"t  - Timer, Aufnahme nach 10s\n")
   txt.insert(END,"v  - Vorschau ohne Speichern der Aufnahme\n")
   txt.insert(END,"s/r- Shutdown/Reboot Kamera\n")
   txt.insert(END,"l  - Löschen der Files im aktuellen Verzeichnis\n")
   txt.insert(END,"f  - Formatieren (Bildverzeichnisse löschen)\n")
   txt.insert(END,"u  - Upload des aktuellen Verzeichnis per FTP\n")
   txt.insert(END,"h  - Hilfe\n")
   txt.insert(END,"0  - ISO Einstellung 0(auto) bis 8(800)\n")
   txt.insert(END,"i  - Voreinstellung für Infrarot\n")
   txt.insert(END,"n  - Normale / Standardeinstellung\n")
   txt.see(END)

   # main functions
   win.bind('a',press_a)
   win.bind('t',press_t)
   win.bind('v',press_v)
   win.bind('s',press_s)
   win.bind('l',press_l)
   win.bind('f',press_f)
   win.bind('u',press_u)
   win.bind('h',press_h)

   win.bind('z',press_z)

   win.bind('r',press_r)

   # iso sets
   win.bind('0',press_num0) # automatic 
   win.bind('1',press_num1) # ISO 100
   win.bind('2',press_num2)
   win.bind('3',press_num3)
   win.bind('4',press_num4)
   win.bind('5',press_num5)
   win.bind('6',press_num6)
   win.bind('7',press_num7)
   win.bind('8',press_num8) # ISO 800

   win.bind('i',press_i)    # Infrarot Preset
   win.bind('n',press_n)    # Normal / Default Preset

   win.mainloop()

else:

   global done
   done = False
   key = ' '

   while not done:

      if tastmode:

         key = raw_input()
         if key   == 'a':
           press_a(0)
         elif key == 't':
           press_t(0)
         elif key == 'v':
           press_v(0)
         elif key == 's':
           press_s(0)
         elif key == 'l':
           press_l(0)
         elif key == 'f':
           press_f(0)
         elif key == 'u':
           press_u(0)
         elif key == 'h':
           press_h(0)

         elif key == 'r':
           press_r(0)

         elif key == '0':
           press_num0(0)
         elif key == '1':
           press_num1(0)
         elif key == '2':
           press_num2(0)
         elif key == '3':
           press_num3(0)
         elif key == '4':
           press_num4(0)
         elif key == '5':
           press_num5(0)
         elif key == '6':
           press_num6(0)
         elif key == '7':
           press_num7(0)
         elif key == '8':
           press_num8(0)

         elif key == 'i':
           press_i(0)
         elif key == 'n':
           press_n(0)

      else: time.sleep(1)

      if GPIO.input(KEY_UP_PIN) == 0:
        press_h(0)
      if GPIO.input(KEY_LEFT_PIN) == 0:
        press_a(0)
      if GPIO.input(KEY_RIGHT_PIN) == 0:
        press_v(0)
      if GPIO.input(KEY_DOWN_PIN) == 0:
        press_u(0)
      if GPIO.input(KEY_PRESS_PIN) == 0:
        press_t(0)
      if GPIO.input(KEY1_PIN) == 0:
        press_s(0)
      if GPIO.input(KEY2_PIN) == 0:
        press_f(0)
      if GPIO.input(KEY3_PIN) == 0:
        press_l(0)

#-----------------------------------------------------------------------------


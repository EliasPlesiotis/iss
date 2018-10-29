import urllib.request
import os
import json
import time
import threading
import tkinter
import math


global window 
window = tkinter.Tk()

def iss_pos():#locate the iss
    iss = json.loads(urllib.request.urlopen('http://api.open-notify.org/iss-now.json').read())
    return float(iss['iss_position']['latitude']), float(iss['iss_position']['longitude'])

def locate():#locate user
    i = json.loads(urllib.request.urlopen('http://ip-api.com/json/?fields=520191&lang=en').read())
    return float(i['lat']), float(i['lon'])

def speed(l, func):#calculate the speed of the iss(always run as deamon)

    places = []

    while 1:
        places.append(func())
        time.sleep(5)
        places.append(func())
        speed = math.floor((2*math.pi*408000*(math.sqrt((places[0][0]-places[1][0])**2+(places[0][1]-places[1][1])**2)/360))/5)
        
        l.configure(text = 'Iss speed: '+str(speed)+'km/s', font = 'Arial')
        places.clear()



def generate_location(l, im, func):#find the position of the iss(always run as deamon)

    while 1:
        l.configure(text = 'Iss Position:'+str(func()[0])+', '+str(func()[1]), font = 'Arial')
        im.place(x = math.floor(512+240+iss_pos()[1]*(1024/360)), y = math.floor(512/2-iss_pos()[0]*(512/180)))
        time.sleep(2)


def main():

    #tkinter declarations
    window.geometry('1300x500')
    my_location = tkinter.Label(window, bg = 'Light Blue', text='Your Position: '+str(locate()[0])+', '+str(locate()[1]), font = 'Arial')
    iss = tkinter.Label(window,bg = 'Light Blue', text='Iss Position: '+str(iss_pos()[0])+', '+str(iss_pos()[1]), font = 'Arial')
    s = tkinter.Label(window, bg = 'Light Blue', text = 'calculating iss speed', font = 'Arial')
    os.chdir(os.getcwd())#just to be sure
    map = tkinter.PhotoImage(file = 'land_shallow_topo_2048.gif')
    pin = tkinter.PhotoImage(file = '660011-location-512.png')
    sat = tkinter.PhotoImage(file = 'main-qimg-c466c1167580cf32d8b1ddbe52a839bc.png')
    map = map.subsample(2, 2)
    pin = pin.subsample(32, 32)
    sat = sat.subsample(12, 8)
   
    bg = tkinter.Label(window, image = map)
    me = tkinter.Label(window, image = pin)
    satellite = tkinter.Label(window, image = sat)

    #threads declarations
    loc = threading.Thread(target = generate_location, args = (iss,satellite, iss_pos))
    sp = threading.Thread(target = speed, args = (s, iss_pos))

    #tkinter elements positioning
    window.title('Finding Iss')
    window.configure(background = 'Light Blue')
    my_location.grid(column=0, row=5)
    iss.grid(column=0, row=7)
    s.grid(column = 0, row = 9)
    #tkinter image positioning
    me.place(x = 512+240+math.floor(locate()[1]*(1024/360)), y = 512/2-math.floor(locate()[0]*(512/180)+16))
    satellite.place(x = math.floor(512+240+iss_pos()[1]*(1024/360)), y = math.floor(512/2-iss_pos()[0]*(512/180)))
    bg.place(x = 250, y = 0)

    #starting threads
    loc.start()
    sp.start()


    window.mainloop()


if __name__ == '__main__':
    main()

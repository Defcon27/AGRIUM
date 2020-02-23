import RPi.GPIO as gpio
import time
import sys
import Tkinter as tk
import random
import Adafruit_DHT
import time
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)


def init() :
	gpio.setmode(gpio.BOARD)
	gpio.setup(31, gpio.OUT)
	gpio.setup(33, gpio.OUT)
	gpio.setup(35, gpio.OUT)
	gpio.setup(37, gpio.OUT)


def backward(tf) :
  #gpio.output(31, False)
  #gpio.output(33, False)
  gpio.output(35, True)
  gpio.output(37, False)
  time.sleep(tf)
  gpio.output(35, False)
  #gpio.cleanup()


def forward(tf) :
  #gpio.output(31, False)
  #gpio.output(33, False)
  gpio.output(35, False)
  gpio.output(37, True)
  time.sleep(tf)
  gpio.output(37, False)
  #gpio.cleanup()


def right(tf) :
  gpio.output(31, True)
  gpio.output(33, False)
  #time.sleep(0.2)
  #gpio.output(35, False)
  #gpio.output(37, True)
  #time.sleep(tf)
  #gpio.cleanup()

def left(tf) :
  gpio.output(31, False)
  gpio.output(33, True)
  #time.sleep(0.2)
  #gpio.output(35, False)
  #gpio.output(37, True)
  #time.sleep(tf)
  #gpio.cleanup()
  





def distance(): # gets obstacle distace (returns float)
	try:
		TRIG = 16
		ECHO = 18

		gpio.setup(TRIG,gpio.OUT)
		gpio.setup(ECHO,gpio.IN)
		
		gpio.output(TRIG, True)
		time.sleep(0.00001)
		gpio.output(TRIG, False)

		while gpio.input(ECHO) == False:
			start = time.time()

		while gpio.input(ECHO) == True:
			end = time.time()

		sig_time = end-start
		#CM:
		distance = sig_time/ 0.000058
		#print('Distance: {} centimeters'.format(distance))
		gpio.cleanup()

		return distance
	except:
		print("except")
		return 10
		gpio.cleanup()

def dht(): #gets temp and humid returns [humid,temp]
	humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	
	return [humidity,temperature]


def check(tf):
	init()
	dist=distance()
	
	if dist<40:
		print("Dead",)
		
		x=random.randrange(0,2)
		
		if(x==0):
			init()
			left(tf)
			backward(tf)
		else:
			init()
			right(tf)
			backward(tf)
		
		dist=distance()
		if dist<15:
			init()
			backward(1)
			init()
			forward(tf)

def autonomy():
	tf=0.03
	
	x=random.randrange(0,3)
	
	if x==0:
		for y in range(30):
			check(tf)
			init()
			forward(0.2)
	elif(x==1):
		for y in range(30):
			check(tf)
			init()
			left(tf)
			forward(0.2)
	elif(x==2):
		for y in range(30):
			check(tf)
			init()
			right(tf)
			forward(tf)
		




def key_input(event) :
	init()
	print 'Key : ',event.char
	key_press = event.char
	sleep_time = 0.025
	
	if key_press.lower() == 'w':
		forward(sleep_time)
	elif key_press.lower() == 's':
		backward(sleep_time)
	elif key_press.lower() == 'a':
		left(sleep_time)
	elif key_press.lower() == 'd':
		right(sleep_time)
	elif key_press.lower() == 'z':
		for i in range(30):
			autonomy()
	elif key_press.lower() == 'x':
		gpio.cleanup()
		sys.exit()
	else:
		gpio.cleanup()
		
		
command = tk.Tk()
command.bind('<KeyPress>',key_input)
command.mainloop()



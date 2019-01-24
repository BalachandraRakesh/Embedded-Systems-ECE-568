//The below code was used for the final project in ECE56800
//Initialization of the camera,led and buttons
from picamera import PiCamera
from time import sleep
import cv2
import math
import RPi.GPIO as GPIO
ledr= 11
ledy= 13
ledg = 15
button1 = 18
button2 = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledr, GPIO.OUT,initial=0)
GPIO.setup(ledy, GPIO.OUT,initial=0)
GPIO.setup(ledg, GPIO.OUT,initial=0)
GPIO.setup(button1, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button2,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
//Here we compute the eucledian distance for every pixel of the reference image(taken before foul happens) and the second image(taken after the foul happens)
def compare():
	print('Comparing...')
	GPIO.output(ledy,GPIO.HIGH)
	img1 = cv2.imread('pic1.jpg')
	size1 =  list(img1.shape)
	img1 = list(img1)
	##size = [480,640,3]
	img2 = cv2.imread('pic2.jpg')
	size2 =  img2.shape
	img2 = list(img2)
	count = 0
	for i in range(size1[0]):
		for j in range(size1[1]):
			d = int(math.sqrt(((int(img1[i][j][0])) - (int(img2[i][j][0])))**2 + ((int(img1[i][j][1])) - (int(img2[i][j][1])))**2 + ((int(img1[i][j][2])) - (int(img2[i][j][2])))**2))
			if(d > 55):
				count = count + 1
//If the eucledian distance 'd' is greater than our threshold value '55' then we count them as different pixels
	print'The number of different pixels are :',count
	GPIO.output(ledy,GPIO.LOW)
//If the total number of different pixels is greater than our threshold '2000' then the two images are different and the red led lights up 
	if(count> 2000):
		GPIO.output(ledr,GPIO.HIGH)
		print('The balls are not in the right place')
		sleep(8)
		GPIO.output(ledr,GPIO.LOW)
//If the total number of different pixels is lesser than our threshold '2000' then the two images are similar and the green led lights up 
	else:
		GPIO.output(ledg,GPIO.HIGH)
		print('The balls are back in the right place')
		sleep(8)
		GPIO.output(ledg,GPIO.LOW)
while True:
	if(GPIO.input(button1) ==1):
		camera = PiCamera()
		camera.resolution = (640,480)
		camera.start_preview()
		sleep(5)
		camera.capture('/home/pi/Desktop/Embedded/pic1.jpg')
		camera.stop_preview()
		camera.close()     
    #button2.wait_for_press()
    	elif(GPIO.input(button2) ==1):
        	camera = PiCamera()
		camera.start_preview()
		camera.resolution = (640,480)
		sleep(5)
		camera.capture('/home/pi/Desktop/Embedded/pic2.jpg')
		camera.stop_preview()
		camera.close()
		compare()						
GPIO.setwarnings(False)
GPIO.cleanup()
     

import time
from gpiozero import CamJamKitRobot
from gpiozero import DistanceSensor
#import plot
import socket
from pid import Pid
import threading

echoPin = 18
triggerPin = 17
leftmotorspeed = 0
rightmotorspeed = 0

# setup server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("192.168.99.23", 8080)
sock.bind(server_address)
sock.listen(1)

sensor = DistanceSensor(echo = echoPin, trigger = triggerPin)
robot = CamJamKitRobot()
sensor.distance
stop_thread = False

pidController = Pid(1.5, 0.1, 1, 5)

def control():

	avg = 0
	reference = 20
	left = -0.3
	right = -0.29
	left_0 = 0.3
	right_0 = 0.29
	last_avg = 0
	distanceVal = []
	leftMotorVal = []
	rightMotorVal = []
	global stop_thread

	while(stop_thread == False):
		sum = 0

		for i in range(0, 100):
			sum += getDist()

		avg =  sum / 100
		if abs(last_avg - avg) > 30:
			avg = 10
		#If increasing -> closer to wall, if decreasing -> longer from wall
		diff = reference - avg
		print("current avg: {}".format(avg))

		#avg_diff = diff - last_diff
		controlVal = pidController.p(diff)

		#controlVal = controlVal
		controlVal = controlVal / 100
		print("ControlVal {}, Diff {}".format(controlVal, diff))
		left = left_0 + (left_0 * controlVal)
		right = right_0 - (right_0 * controlVal) #dette virker nogenlunde men kan tunes bedre, men mit gulv er lort
		print("left {}, right {}".format(left, right))
		if(right > 1):
			right = 1
		elif(right < -1):
			right = 1	
		
		if(left > 1):
			left = 1
		elif(left < -1):
			left = 1
		
		run(-left, -right)
		distanceVal.append(avg)
		leftMotorVal.append(left)
		rightMotorVal.append(right)
		last_avg = avg
		time.sleep(0.2)
	# stop the motor		
	leftmotorspeed = 0
	rightmotorspeed = 0
	motorforward = (leftmotorspeed, rightmotorspeed)
	robot.value = motorforward

#Robot is ready
#def plotCall(distanceVal, leftMotorVal, rightMotorVal):
	#plot.plotFunc(distanceVal, leftMotorVal, rightMotorVal)

def run(right, left):
	motorforward = (left, right)
	robot.value = motorforward

def getDist():
	return sensor.distance * 100

def start():
	process = threading.Thread(target = control)
	global stop_thread
	stop_thread = False
	# start wall following behavior
	process.start()

def stop():
	global stop_thread
	stop_thread = True
	
def getmotors():
	return ("Left motor speed: {}, Right motor speed: {}".format(leftmotorspeed, rightmotorspeed))

print("The robot is ready to go")
while True:
	connection, client_address = sock.accept()
	try:
		data = connection.recv(16)
		command = data.decode().rstrip("\n").split(" ")
		returnVar = ""

		print("command is {}".format(command))

		if  command[0] == "start":
			start()
			returnVar = "Started\n"
		elif command[0] == "stop":
			stop()
			returnVar = "Stopped\n"
		elif command[0] == "getdist":
			distanceVar = getDist()
			returnVar = "The distance is: {}\n".format(distanceVar)
		elif command[0] == "getmotors":
			returnVar = "Get Motors {}\n".format(getmotors())
		elif command[0] == "run":
			run(float(command[1]), float(command[2]))
			returnVar = "run with left: {}, right: {}\n".format(command[1], command[2])
		else:
			print("invalid input")

		if data:
			connection.sendall(bytearray(returnVar, "utf-8"))
		else:
			break

	finally:
		connection.close()

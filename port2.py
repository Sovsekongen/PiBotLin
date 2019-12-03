
import time
from gpiozero import CamJamKitRobot
from gpiozero import DistanceSensor
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
stop_thread = True

pidController = Pid(1.5, 0.1, 1, 5)

def control():

	avg = 0
	reference = 20
	left = -0.3
	right = -0.29
	left_0 = 0.3
	right_0 = 0.29
	last_avg = 0
	next_last_avg = 0
	current_avg = 0
	global stop_thread

	while(stop_thread == False):
		sum = 0

		for i in range(0, 100):
			sum += getDist()

		avg =  sum / 100
		# if the angle is to big towards wall or away from the wall, the sensor will change to 100 and therefor this check, so
		print(avg)
		current_avg = avg
		if avg == 100:
			if last_avg-next_last_avg < 0:
				current_avg = 10
			else:
				current_avg = 30
		#If diffence bigger than 0 close to wall if away from wall smaller than 0
		diff = reference - current_avg

		controlVal = pidController.p(diff)

		controlVal = controlVal / 100
		left = left_0 + (left_0 * controlVal)
		right = right_0 - (right_0 * controlVal) 
		if(right > 1):
			right = 1
		elif(right < -1):
			right = 1	
		
		if(left > 1):
			left = 1
		elif(left < -1):
			left = 1
		
		run(-left, -right)
		next_last_avg = last_avg
		last_avg = current_avg
		time.sleep(0.2)
	# stop the motor		
	leftmotorspeed = 0
	rightmotorspeed = 0
	motorforward = (leftmotorspeed, rightmotorspeed)
	robot.value = motorforward

def run(right, left):
	motorforward = (left, right)
	robot.value = motorforward

def getDist():
	return sensor.distance * 100

def start():
	process = threading.Thread(target = control)
	global stop_thread
	if stop_thread == False:
		print("already started")
	else:	
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

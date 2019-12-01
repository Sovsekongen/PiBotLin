import matplotlib
import matplotlib.pyplot as plt
from time import sleep

matplotlib.use('tkagg')
def plotFunc(distanceVal, leftVal, rightVal):
	plt.subplot(2, 1, 1)
	plt.title("Distance to wall")
	plt.plot(range(0, len(distanceVal)), distanceVal, color = 'red', label = "Distance to Wall")
	plt.xlabel("Nr. Iterations")
	plt.ylabel("Distance [CM]")
	plt.subplot(2, 1, 2)
	plt.title("Motor Values")
	plt.plot(range(0, len(leftVal)), leftVal, color = 'blue', label = "Left Motor Value")
	plt.plot(range(0, len(rightVal)), rightVal, color = 'green', label = "Right Motor Value")
	plt.xlabel("Nr. Iterations")
	plt.ylabel("Distance")
	plt.legend()

	plt.show()
	return None

#print("Hello!")
#plotFunc(range(10, 19), range(20, 29), range(30, 39))

# PiBot Group 23
For completing this project we developed three python scripts. One for controlling the robot, one for plotting the results and one for implementation of a PID-controller that controls the robot. Other than the four necessary commands we mainly use a fifth command namely run, that takes two paramers, one for each motor.

For controlling the robot a P-controller was implemented, which handles checking the distance to a reference of 20 centimeters. It was tuned by hand. The controller runs a python thread concurrent to the tcp server. We did this to make it possible to send other commands to the robot, while the control-part was running.

ADHOC connects automatically to a network of the IP-address 192.168.99.23:8080 from where it accepts commands running. On the PiBot a python-tcp server is running, which accepts the following commands: stop, start, getdist, getmotors and run, where run is a command that takes two parameters one for each motor.

For booting with the ADHOC network activated we added the interface to /etc/rc.local. The 4 commands are:
sudo iw wlan0 set type ibss
sudo ip link set wlan0 up
sudo iw wlan0 ibss join pibot 2417
sudo ip address add 192.168.99.23/16 dev wlan0

The way we send commands:

echo <COMMAND> | socat - tcp:192.168.99.23:8080

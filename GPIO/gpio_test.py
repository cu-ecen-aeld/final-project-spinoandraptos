try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    
# Set GPIO mode as using Broadcom SOC
# Use BCM pin 17 for push button
# Reference: https://pinout.xyz/pinout/pin11_gpio17/
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(17, GPIO.IN)

# Constantly check for button press
while True:
	buttonPressed = GPIO.input(17)
	if buttonPressed:
		print("Button Pressed")
	else:
		print("Button Released")
	

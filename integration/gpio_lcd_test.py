try:
	from RPLCD.gpio import CharLCD
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPLCD!")
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(11, GPIO.IN)

# Write to LCD in 8-bit data mode
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],
              numbering_mode=GPIO.BOARD)
              
# Set cursor position to the top row and print "DUMMY"
print("Initial write:")
lcd.cursor_pos = (0, 0) 
lcd.write_string(u'Button Status:')

# Constantly check for button press
while True:
	buttonPressed = GPIO.input(17)
	if buttonPressed:
		print("Button Pressed")
		lcd.cursor_pos = (1, 0) 
		lcd.write_string(u'Button Pressed!')
	else:
		print("Button Released")
		lcd.cursor_pos = (1, 0) 
		lcd.write_string(u'Button Released!')
		

try:
	from RPLCD.gpio import CharLCD
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPLCD!")
   
# Write to LCD in 8-bit data mode
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],
              numbering_mode=GPIO.BOARD)

# Set cursor position to the top row and print "DUMMY"
print("printing: Dummy")
lcd.cursor_pos = (0, 0) 
lcd.write_string(u'DUMMY:')

# Set cursor position to the bottom row and print "Dummy Value"
print("printing: Dummy value")
lcd.cursor_pos = (1, 0) 
lcd.write_string(u'Score: Dummy')

try:
	from RPLCD.gpio import CharLCD
except RuntimeError:
	print("Error importing RPLCD!")
	
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPIGPIO!")
	
try:
	import pyaudio
except RuntimeError:
	print("Error importing pyaudio!")
    
try:
	import wave
except RuntimeError:
	print("Error importing wave!")
	
from time import sleep

PUSH_BUTTON = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(PUSH_BUTTON, GPIO.IN)

# Write to LCD in 8-bit data mode
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],
              numbering_mode=GPIO.BOARD)
              
lcd.cursor_pos = (0, 0) 
lcd.write_string(u'Press to Record!')

# Continuous stream is broken down into chunks 
# Buffer sample size for each chunk to lighten processing workload
# Prevents memory leak with small RAM in embedded systems
CHUNK = 512
# 16 bit signed int for binary sound representation
FORMAT = pyaudio.paInt16
OUTPUT_PATH = "/tmp/test.wav"
DEVICE_IDX, CHANNELS, RATE = None, None, None
mic_name = 'USB PnP Sound Device'
recording = False
frames = []
stream = None

print('setting up mic')
p = pyaudio.PyAudio()

devices = p.get_device_count()
for i in range(devices):
# Get the device info
	device_info = p.get_device_info_by_index(i)
	name = str(device_info.get('name'))
	if mic_name in name:
		DEVICE_IDX = device_info.get('index')
		CHANNELS = device_info.get('maxInputChannels')
		RATE = int(device_info.get('defaultSampleRate'))
		print(DEVICE_IDX)
		print(CHANNELS)
		print(RATE)
		print('mic set up successfully')
	
def button_event(channel):

	#Rising edge
	if GPIO.input(PUSH_BUTTON):
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Recording audio!')
		recording = True
		
		# Input stream initiation
		global stream 
		stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input_device_index=DEVICE_IDX,
		    input=True,
		    frames_per_buffer=CHUNK)

		print("* recording")
		
	#Falling edge
	else:
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Done recording!')
		recording = False
		print("* stop recording")
		
		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(OUTPUT_PATH, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		print("Saved")
		sleep(5) 

		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Press to Record!')
		
GPIO.add_event_detect(PUSH_BUTTON, GPIO.BOTH, callback=button_event, bouncetime=200)		
	
while True:
	if recording:
		data = stream.read(CHUNK, exception_on_overflow=False)
		frames.append(data)




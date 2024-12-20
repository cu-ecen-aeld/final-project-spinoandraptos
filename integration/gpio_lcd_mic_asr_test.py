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
	
try:
	from pocketsphinx import AudioFile
except RuntimeError:
	print("Error importing pocketsphinx!")

import random
from time import sleep
from pyaline import lookup_phonemes_score
import re
from collections import defaultdict
from itertools import product as iterprod

def recurse_find_phoneme(s, arpabet):
	if s in arpabet:
		return arpabet.get(s)
	middle = len(s)/2
	partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
	for i in partition:
		pre, suf = (s[:i], s[i:])
		if pre in arpabet and recurse_find_phoneme(suf, arpabet) is not None:
			return [x+y for x,y in iterprod(arpabet[pre], recurse_find_phoneme(suf, arpabet))]

def grade_phonemes(transcription, arpabet, reference_word):
	total_phoneme_score = 0
	print("Reference:", reference_word)
	print("Transcription:", transcription)
	ref_phonemes = arpabet.get(reference_word) 
	print("Ref phonemes", ref_phonemes)
	
	# Edge Condition : When user input contains multiple words, join together into one word
	transcription = transcription.strip()
	if " " in transcription:
		transcription = transcription.replace(" ", "")
	
	if transcription == reference_word:
		total_phoneme_score = 100 #full marks
	else:
		user_phonemes = recurse_find_phoneme(transcription, arpabet)
		print("User Phenomes", user_phonemes)
		for i in range(len(ref_phonemes[0])):
			if i < len(user_phonemes[0]):
				ref_phoneme = ref_phonemes[0][i]
				ref_phoneme = ''.join([i for i in ref_phoneme if not i.isdigit()])
				user_phoneme = user_phonemes[0][i]
				user_phoneme = ''.join([i for i in user_phoneme if not i.isdigit()])
				distance = lookup_phonemes_score(user_phoneme, ref_phoneme)
				total_phoneme_score += distance
				total_phoneme_score = total_phoneme_score/len(ref_phonemes[0]) 

	return total_phoneme_score * 100

start_recording = False
stop_recording = False

def button_event(channel):
	
	#Rising edge
	if GPIO.input(PUSH_BUTTON):
		global start_recording
		start_recording = True
		
	#Falling edge
	else:
		global stop_recording
		stop_recording = True
		
TEST_WORDS = ["backpack", "book","bookcase","bottle","chair", "clock", "desk", "door", "flag", "laptop", "apple", "banana", "bed", "bowl", "box", "bread", "glasses", "umbrella", "lantern", "scissors", "bicycle", "cupboard", "cabbage"]

reference_word = random.choice(TEST_WORDS)

PUSH_BUTTON = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Write to LCD in 8-bit data mode
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23],
              numbering_mode=GPIO.BOARD)
              
lcd.cursor_pos = (0, 0) 
lcd.write_string(u'Loading...')


# Continuous stream is broken down into chunks 
# Buffer sample size for each chunk to lighten processing workload
# Prevents memory leak with small RAM in embedded systems
CHUNK = 512
# 16 bit signed int for binary sound representation
FORMAT = pyaudio.paInt16
OUTPUT_PATH = "/tmp/test.wav"
DEVICE_IDX, CHANNELS, RATE = None, None, None
mic_name = 'USB PnP Sound Device'

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
p.terminate()
p = None

dictionary = []
comment_string="#"	
with open('cmudict.dict', 'r') as f:
    for line in f:
        parts = []
        if comment_string in line:
            parts = line.strip().split(comment_string)[0].split()
        else:
            parts = line.strip().split()
            thing = re.sub(r"\(\d+\)$", "", parts[0])
            dictionary.append((thing, parts[1:]))

cmudict = defaultdict(list)
for key, value in dictionary:
	cmudict[key].append(value)
	
lcd.cursor_pos = (0, 0) 
lcd.write_string(u'Press to Record!')
lcd.cursor_pos = (1, 0) 
lcd.write_string(reference_word)
	
GPIO.add_event_detect(PUSH_BUTTON, GPIO.BOTH, callback=button_event, bouncetime=500)	
recording = False
frames = []
stream = None	
	
while True:
	if start_recording:
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Recording audio!')
		frames = []
		# Input stream initiation
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input_device_index=DEVICE_IDX,
		    input=True,
		    frames_per_buffer=CHUNK)
		start_recording = False
		recording = True
		print("* recording")
		    
	elif stop_recording:
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
	
		print("Processing starts")
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Processing!     ')
		audio = AudioFile(
		    audio_file=OUTPUT_PATH,  # Replace with your audio file path
		)
		transcription = ""
		# Iterate over the audio file and get recognized text
		for phrase in audio:
			hypothesis = str(phrase)
			transcription = transcription + hypothesis + " "
				
		score = grade_phonemes(str(transcription), cmudict, reference_word)
		score = round(score, 2) 

		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'                ')
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Score:')
		lcd.cursor_pos = (0, 7) 
		lcd.write_string(str(score))
		sleep(10)
		
		lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)
		reference_word = random.choice(TEST_WORDS)
		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Press to Record!')
		lcd.cursor_pos = (1, 0) 
		lcd.write_string(u'                ')
		lcd.cursor_pos = (1, 0) 
		lcd.write_string(reference_word)
		
		stop_recording =  False
		
	elif recording:
		data = stream.read(CHUNK, exception_on_overflow=False)
		frames.append(data)




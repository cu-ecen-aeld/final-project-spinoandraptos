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
	import cmudict
except RuntimeError:
	print("Error importing cmudict!")
	
try:
	import whisper
except RuntimeError:
	print("Error importing whisper!")
	
from time import sleep
from pyaline import lookup_phonemes_score


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

arpabet = cmudict.dict()
reference_word = "laptop" #dummy word for testing: laptop

def recurse_find_phoneme(s, arpabet):
        if s in arpabet:
            return arpabet.get(s)
        middle = len(s)/2
        partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
        for i in partition:
            pre, suf = (s[:i], s[i:])
            if pre in arpabet and recurse_find_phoneme(suf) is not None:
                return [x+y for x,y in iterprod(arpabet[pre], recurse_find_phoneme(suf))]
                
def grade_phonemes(transcription, arpabet):
	total_phoneme_score = 0
	ref_phonemes = arpabet.get(reference_word) 
	print("Ref phonemes", ref_phonemes)
	
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
				total_phoneme_score = total_phoneme_score/len(ref_phonemes[0]) * 100
				
	return total_phoneme_score
	
def get_transcription(audio_path):
	model = whisper.load_model('tiny')
	result = model.transcribe(audio=AUDIO_PATH, language='en', verbose=True)
	transcription = result.get('text', '')
	print("Transcription: ", transcription)
	return transcription
		
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
		
		transcription = get_transcription(OUTPUT_PATH)
		score = grade_phonemes(transcription, arpabet)

		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Score:')
		lcd.write_string(str(score))
		sleep(5)

		lcd.cursor_pos = (0, 0) 
		lcd.write_string(u'Press to Record!')
		
GPIO.add_event_detect(PUSH_BUTTON, GPIO.BOTH, callback=button_event, bouncetime=200)		
	
while True:
	if recording:
		data = stream.read(CHUNK, exception_on_overflow=False)
		frames.append(data)




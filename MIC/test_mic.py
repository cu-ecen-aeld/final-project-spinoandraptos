try:
	import pyaudio
except RuntimeError:
	print("Error importing pyaudio!")
    
try:
	import wave
except RuntimeError:
	print("Error importing pyaudio!")

DEVICE_IDX, CHANNELS, RATE = None, None, None
mic_name = 'USB PnP Sound Device'

def set_device():
	print('setting up mic')
	p = pyaudio.PyAudio()
	while True:
		devices = p.get_device_count()
		for i in range(devices):
		# Get the device info
			device_info = p.get_device_info_by_index(i)
			name = str(device_info.get('name'))
			if mic_name in name:
				DEVICE_IDX = device_info.get('index')
				CHANNELS = device_info.get('maxInputChannels')
				RATE = int(device_info.get('defaultSampleRate'))
				print('mic set up successfully')
                

# Continuous stream is broken down into chunks 
# Buffer sample size for each chunk to lighten processing workload
# Prevents memory leak with small RAM in embedded systems
CHUNK = 1024
# 16 bit signed int for binary sound representation
FORMAT = pyaudio.paInt16
# Duration of recording
RECORD_SECONDS = 5

output_path = "/tmp/test.wav"

def record_audio(output_path:str):
	# Port audio initiation
	p = pyaudio.PyAudio()
	# Input stream initiation
	stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input_device_index  = DEVICE_IDX,
		    input=True,
		    frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	# Read in samples as chunks 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(output_path, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
    
if __name__ == '__main__':
	set_device()
	record_audio()

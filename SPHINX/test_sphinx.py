try:
	from pocketsphinx import AudioFile
except RuntimeError:
	print("Error importing pocketsphinx!")
try:
	import wave
except RuntimeError:
	print("Error importing wave!")
	
try:
	import librosa
except RuntimeError:
	print("Error importing librosa!")
	
input_data, sampling_rate = librosa.load(audio_path, sr=16000)
input_data = np.expand_dims(input_data, axis=0)

AUDIO_PATH = "/tmp/test.wav"
       
# Create an AudioFile object
#audio = AudioFile(
	#audio_file=AUDIO_PATH,  # Replace with your audio file path
#)

# Iterate over the audio file and get recognized text
#for phrase in audio:
	#hypothesis = str(phrase)
	#print(hypothesis)
	
decoder.start_utt()
stream = open(AUDIO_PATH, 'rb')
in_speech_bf = False
while True:
	buf = stream.read(args.chunk_size)
	if buf:
		decoder.process_raw(buf, False, False)  # full_utt = False
		if decoder.get_in_speech() != in_speech_bf:
			in_speech_bf = decoder.get_in_speech()
			if decoder.hyp() is not None:
			hypothesis.append(decoder.hyp().hypstr)
			[bag_of_words.append(seg.word) for seg in decoder.seg() if seg.word not in buzz_words]
			decoder.end_utt()
			decoder.start_utt()
    
   

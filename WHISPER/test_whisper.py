try:
	import whisper
except RuntimeError:
	print("Error importing whisper!")

AUDIO_PATH = "/tmp/test.wav"

model = whisper.load_model('tiny')
result = model.transcribe(audio=AUDIO_PATH, language='en', verbose=True)
print(result.get('text', ''))



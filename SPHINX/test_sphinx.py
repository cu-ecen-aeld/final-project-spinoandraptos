try:
	from pocketsphinx import Decoder
except RuntimeError:
	print("Error importing pocketsphinx!")
try:
	import wave
except RuntimeError:
	print("Error importing wave!")

AUDIO_PATH = "/tmp/test.wav"

with wave.open(AUDIO_PATH, "rb") as audio:
    decoder = Decoder(samprate=audio.getframerate())
    decoder.start_utt()
    decoder.process_raw(audio.getfp().read(), full_utt=True)
    decoder.end_utt()
    print(decoder.hyp().hypstr)

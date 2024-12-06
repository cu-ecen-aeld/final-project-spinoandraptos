try:
	from pocketsphinx import AudioFile
except RuntimeError:
	print("Error importing pocketsphinx!")
try:
	import wave
except RuntimeError:
	print("Error importing wave!")

AUDIO_PATH = "/tmp/test.wav"
       
# Create an AudioFile object
audio = AudioFile(
    audio_file=AUDIO_PATH,  # Replace with your audio file path
)

# Iterate over the audio file and get recognized text
for phrase in audio:
    hypothesis = str(phrase)
    print(hypothesis)
    
   

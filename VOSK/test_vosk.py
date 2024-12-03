try:
	import json
except RuntimeError:
	print("Error importing json!")
try:
	from vosk import Model, KaldiRecognizer
except RuntimeError:
	print("Error importing vosk!")

AUDIO_PATH = "/tmp/test.wav"
model = Model("/usr/bin/vosk-model-small-en-us-0.15")

wf = wave.open(AUDIO_PATH, "rb")
rec = KaldiRecognizer(model, 44100)

result = ''
last_n = False

while True:
    data = wf.readframes(44100)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())

        if res['text'] != '':
            result += f" {res['text']}"
            last_n = False
        elif not last_n:
            result += '\n'
            last_n = True

res = json.loads(rec.FinalResult())
result += f" {res['text']}"

print(result)

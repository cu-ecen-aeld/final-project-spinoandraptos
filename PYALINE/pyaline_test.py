try:
	import cmudict
except RuntimeError:
	print("Error importing cmudict!")
	
from pyaline import lookup_phonemes_score

def recurse_find_phoneme(s, arpabet):
	if s in arpabet:
		return arpabet.get(s)
	middle = len(s)/2
	partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
	for i in partition:
		pre, suf = (s[:i], s[i:])
		if pre in arpabet and recurse_find_phoneme(suf) is not None:
			return [x+y for x,y in iterprod(arpabet[pre], recurse_find_phoneme(suf))]

def grade_phonemes(transcription, arpabet, reference_word):
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

reference_word = "library"
arpabet = cmudict.dict()
transcription = [["leebwary"]]
score = grade_phonemes(transcription, arpabet, reference_word)
print(score)
	

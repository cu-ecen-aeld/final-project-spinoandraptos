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
				total_phoneme_score = total_phoneme_score/len(ref_phonemes[0]) 

	return total_phoneme_score * 100
	
dict = []
comment_string="#"	
with open('cmudict.dict', 'r') as f:
    parts = []
    for line in f:
        if comment_string:
            parts = line.strip().split(comment_string)[0].split()
        else:
            parts = line.strip().split()
        thing = re.sub(r"\(\d+\)$", "", parts[0])
        dict.append((thing, parts[1:]))

cmudict = defaultdict(list)
for key, value in dict:
    cmudict[key].append(value)

reference_word = "library"
transcription = "leebwary"
score = grade_phonemes(transcription, cmudict, reference_word)
print(score)
	

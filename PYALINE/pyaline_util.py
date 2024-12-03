import re
Infinity = float('inf')

multivalued_features = {
                  'place': {'bilabial': 100,
				  'labiodental': 95,
				  'dental': 90,
				  'alveolar': 85,
				  'velar + bilabial': 80,
				  'palato-alveolar': 75,
				  'palatal': 70,
                          'velar + palatal': 64,
				  'velar': 60,
				  'uvular': 50,
				  'pharyngeal': 30,
				  'glottal': 10
                                  },
			'manner': {'stop': 100,
				   'affricate': 90,
				   'fricative': 80,
				   'approximant': 60,
                           'trill': 50,
				   'high vowel': 40,
                           'mid vowel + high vowel': 28,
				   'mid vowel': 20, 
                           'low vowel + high vowel': 16,  
				   'low vowel': 0
                                   },
			'high': {'high': 100,
                         'mid + high': 70,
				 'mid': 50,
                         'low + high': 40,
				 'low': 0
                                 },
			'back': {'front': 100,
                         'central + front': 70,
				 'central': 50,
                         'back + front': 40,
				 'back': 0
                                 }
			}

# Following the feature specification of https://sites.google.com/site/similaritymatrices/phonological-features/english-feature-specifications?authuser=0
phonemes_features = {
            'AA': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['low vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['low'],
                  'back': multivalued_features['back']['central'],
                  'round': 0,
                  'long': 100
                  },
            'AE': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['low vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['low'],
                  'back': multivalued_features['back']['front'],
                  'round': 0,
                  'long': 0
                  },
            'AH': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['mid vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid'],
                  'back': multivalued_features['back']['central'],
                  'round': 0,
                  'long': 0
                  },
            'AO': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['low vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['low'],
                  'back': multivalued_features['back']['central'],
                  'round': 100,
                  'long': 100
                  },
            'AW': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['low vowel + high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['low + high'],
                  'back': multivalued_features['back']['back'],
                  'round': 40,
                  'long': 100
                  },
            'AY': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['low vowel + high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['low + high'],
                  'back': multivalued_features['back']['central + front'],
                  'round': 0,
                  'long': 100
                  },
            'B': {
                  'place': multivalued_features['place']['bilabial'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['low + high'],
                  # 'back': multivalued_features['back']['central + front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'CH': {
                  'place': multivalued_features['place']['palato-alveolar'],
		      'manner': multivalued_features['manner']['affricate'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['low + high'],
                  # 'back': multivalued_features['back']['central + front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'D': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['low + high'],
                  # 'back': multivalued_features['back']['central + front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'DH': {
                  'place': multivalued_features['place']['dental'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['low + high'],
                  # 'back': multivalued_features['back']['central + front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'EH': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['mid vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid'],
                  'back': multivalued_features['back']['front'],
                  'round': 0,
                  'long': 0
                  },
            'ER': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['mid vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid'],
                  'back': multivalued_features['back']['central'],
                  'round': 0,
                  'long': 100
                  },
            'EY': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['mid vowel + high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid + high'],
                  'back': multivalued_features['back']['front'],
                  'round': 0,
                  'long': 100
                  },
            'F': {
                  'place': multivalued_features['place']['labiodental'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'G': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'HH': {
                  'place': multivalued_features['place']['glottal'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'IH': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['mid vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid'],
                  'back': multivalued_features['back']['front'],
                  'round': 0,
                  'long': 0
                  },          
            'IY': {
                  'place': multivalued_features['place']['palatal'],
		      'manner': multivalued_features['manner']['high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['high'],
                  'back': multivalued_features['back']['front'],
                  'round': 0,
                  'long': 100
                  },
            'JH': {
                  'place': multivalued_features['place']['palato-alveolar'],
		      'manner': multivalued_features['manner']['affricate'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'K': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 100,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'L': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['approximant'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 100,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'M': {
                  'place': multivalued_features['place']['bilabial'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 100,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'N': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 100,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'NG': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 100,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['front'],
                  # 'round': 0,
                  # 'long': 100
                  },
            'OW': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['mid vowel + high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid + high'],
                  'back': multivalued_features['back']['back'],
                  'round': 100,
                  'long': 100
                  },
            'OY': {
                  'place': multivalued_features['place']['velar + palatal'],
		      'manner': multivalued_features['manner']['mid vowel + high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['mid + high'],
                  'back': multivalued_features['back']['back + front'],
                  'round': 0,
                  'long': 0
                  },
            'P': {
                  'place': multivalued_features['place']['bilabial'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 100,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'R': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['approximant'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'S': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'SH': {
                  'place': multivalued_features['place']['palato-alveolar'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'T': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['stop'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 100,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'TH': {
                  'place': multivalued_features['place']['dental'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 0, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['mid + high'],
                  # 'back': multivalued_features['back']['back + front'],
                  # 'round': 0,
                  # 'long': 0
                  },
            'UH': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['high'],
                  'back': multivalued_features['back']['back'],
                  'round': 0,
                  'long': 0
                  },
            'UW': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['high vowel'],
                  'vowel': 1,
                  'syllabic': 100, 
                  'voice': 100, 
                  'nasal': 0,
                  # 'lateral': 0,
                  # 'aspirated': 0,
                  'high': multivalued_features['high']['high'],
                  'back': multivalued_features['back']['back'],
                  'round': 100,
                  'long': 100
                  },
            'V': {
                  'place': multivalued_features['place']['labiodental'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['back'],
                  # 'round': 100,
                  # 'long': 100
                  },
            'W': {
                  'place': multivalued_features['place']['velar + bilabial'],
		      'manner': multivalued_features['manner']['approximant'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['back'],
                  # 'round': 100,
                  # 'long': 100
                  },
            'Y': {
                  'place': multivalued_features['place']['velar'],
		      'manner': multivalued_features['manner']['approximant'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['back'],
                  # 'round': 100,
                  # 'long': 100
                  },
            'Z': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['back'],
                  # 'round': 100,
                  # 'long': 100
                  },
            'ZH': {
                  'place': multivalued_features['place']['alveolar'],
		      'manner': multivalued_features['manner']['fricative'],
                  'vowel': 0,
                  'syllabic': 0, 
                  'voice': 100, 
                  'nasal': 0,
                  'lateral': 0,
                  'aspirated': 0,
                  # 'high': multivalued_features['high']['high'],
                  # 'back': multivalued_features['back']['back'],
                  # 'round': 100,
                  # 'long': 100
                  },
            }

class MatrixRow(object):
    def __init__(self, row_length):
        self.row = [ 0 for i in range(row_length)]
        
    def __getitem__(self, index):
        if index < 0:
            return -Infinity
        else:
            return self.row[index]
        
    def __setitem__(self, index, value):
        if index >= 0:
            self.row[index] = value

    def __iter__(self):
        for y in self.row:
            yield y

class Matrix(object):
    def __init__(self, x, y, output_type=None):
        self.rows = []
        self.x_length = x
        self.y_length = y
        for i in range(self.x_length):
            self.rows.append(MatrixRow(self.y_length))
        self.output_type = output_type
            
    def __repr__(self):
        out_string = ""
        if self.output_type == 'r':
            out_string = "c("
        for x in range(self.x_length):
            for y in range(self.y_length):
                if self.output_type == 'r':
                    out_string += "%s, " % self.rows[x][y]
                else:
                    out_string += "%s " % self.rows[x][y]
            out_string = out_string.strip() + "\n"
        out_string = out_string.strip()
        if self.output_type == 'r':
            out_string = re.sub(',$', ')', out_string)
        return out_string

    def __getitem__(self, index):
        if index < 0:
            return [ -Infinity for y in range(self.y_length) ]
        else:
            return self.rows[index]

    def __iter__(self):
        for x in self.rows:
            yield x

    def getX(self):
        return self.x_length

    def getY(self):
        return self.y_length

class AlineMatrix(Matrix):
    def __init__(self, x, y, output_type=None):
        self.x = x
        self.y = y
        super(AlineMatrix, self).__init__(len(x) + 1, len(y) + 1, output_type)

    def __repr__(self):
        out_string = super(AlineMatrix, self).__repr__()
        out_parts = out_string.split("\n")
        # how much space we need for each letter on the y axis
        space = max([len(x['input_string']) for x in self.y]) + 1 

        top_line = " " * (space + 2)
        for i in self.x:
            top_line += i['input_string'] + " "
        new_array = [top_line]
        index = 0

        for j in out_parts:
            if index > 0:
                j = self.y[index]['input_string'] + " " * (space - (len(self.y[index]['input_string']))) + j 
            else:
                j = " " * space + j
            new_array.append(j)
            index += 1
        new_out_string = "\n".join(new_array)
        return new_out_string 
    

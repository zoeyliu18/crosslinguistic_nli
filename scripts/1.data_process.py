#### This script segments, tokenizes and group data from COWSL2H, PELIC and WriCLE into individual folders

#usr/bin/env python3

import io, os, argparse
import pandas as pd
import stanza


def sentence_split(list_of_sentences):

	data = []

	for sent in list_of_sentences:
		if len(sent) != 0 and sent != '\n':
			for i in range(len(sent)):
				c = sent[i]
				if c not in ['¡', '?', '?', '.', '!']:
					data.append(c)
				else:
					data.append(c)
					data.append('-SENT-')

	sentences = ''.join(c for c in data)
	sentences = sentences.split('-SENT-')

	new_sentences = []
	for sent in sentences:
		if len(sent) != 0:
			new_sentences.append(sent)

	return new_sentences

### Read CAES ###

def read_caes(path, output):

	lg_directory = {'Arabe': 'Arabic', 'Chino_mandarin': 'Chinese', 'Frances': 'French', 'Ingles': 'English', 'Portugues': 'Portuguese', 'Ruso': 'Russian'}

	if not os.path.exists(output + 'CAES'):
		os.system('mkdir ' + output + 'CAES')

	for directory in os.listdir(path + 'CAES/'):
		lg = lg_directory[directory]

		if not os.path.exists(output + 'CAES/' + lg):
			os.system('mkdir ' + output + 'CAES/' + lg)

		for file in os.listdir(path + 'CAES/' + directory):
			if os.stat(path + 'CAES/' + directory + '/' + file).st_size != 0:
				essay = []

				with io.open(path + 'CAES/' + directory + '/' + file) as f:
					for line in f:
						essay.append(line.strip())

				new_essay = sentence_split(essay)
				
				with io.open(output + 'CAES/' + lg + '/' + file, 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')

### Read COWSL2H ###

def read_cows(path, output):

	essays = {}

	for file in os.listdir(path + '/cowsl2h/csv/'):
		data = pd.read_csv(path + '/cowsl2h/csv/' + file, encoding = 'utf-8')
		L1 = data['l1 language'].tolist()
		courses = data['course'].tolist()
		texts = data['essay'].tolist()

		for i in range(len(L1)):
			lg = L1[i]
			course = courses[i]
			text = texts[i]
			if lg == 'English' and course not in ['SPA 31', 'SPA 32', 'SPA 33']:
				if lg not in essays:
					essays[lg] = [text]
				else:
					essays[lg].append(text)

	if not os.path.exists(output + 'COWS/'):
		os.system('mkdir ' + output + 'COWS/')

	idx = 1

	for k, v in essays.items():
		if not os.path.exists(output + 'COWS/' + k):
			os.system('mkdir ' + output + 'COWS/' + k)

		for essay in v:
			new_essay = sentence_split(essay)

			with io.open(output + 'COWS/' + k + '/' + str(idx) + '.txt', 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')

			idx += 1


### Read cedel2_learner.csv ###

def read_cedel(path, output):

	essays = {}

	data = pd.read_csv(path + 'cedel2_learner.csv', sep='\t', encoding = 'utf-8')
	L1 = data['L1'].tolist()
	texts = data['Text'].tolist()
	
	for i in range(len(L1)):
		lg = L1[i]
		text = texts[i]
		if lg not in essays:
			essays[lg] = [text]
		else:
			essays[lg].append(text)

	if not os.path.exists(output + 'CEDEL/'):
		os.system('mkdir ' + output + 'CEDEL/')

	idx = 1

	for k, v in essays.items():
		if not os.path.exists(output + 'CEDEL/' + k):
			os.system('mkdir ' + output + 'CEDEL/' + k)

		for essay in v:
			new_essay = sentence_split(essay)

			with io.open(output + 'CEDEL/' + k + '/' + str(idx) + '.txt', 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')

			idx += 1

### Read PELIC_compiled.csv ###

def read_pelic(path, output):

	essays = {}

	data = pd.read_csv(path + 'PELIC_compiled.csv', encoding = 'utf-8')
	L1 = data['L1'].tolist()
	texts = data['text'].tolist()
	
	for i in range(len(L1)):
		lg = L1[i]
		text = texts[i]
		if lg not in essays:
			essays[lg] = [text]
		else:
			essays[lg].append(text)

	if not os.path.exists(output + 'PELIC/'):
		os.system('mkdir ' + output + 'PELIC/')

	idx = 1

	for k, v in essays.items():
		if not os.path.exists(output + 'PELIC/' + k) and k not in ['English', 'Other']:
			os.system('mkdir ' + output + 'PELIC/' + k)

		for essay in v:
			new_essay = sentence_split(essay)

			if k not in ['English', 'Other', 'Russian,Ukrainian']:
				with io.open(output + 'PELIC/' + k + '/' + str(idx) + '.txt', 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')

				idx += 1


### Read text files from WriCLE_formal and WriCLE_informal ###

def read_wricle(path, output):

	if not os.path.exists(output + 'WriCLE_formal'):
		os.system('mkdir ' + output + 'WriCLE_formal')

	if not os.path.exists(output + 'WriCLE_informal'):
		os.system('mkdir ' + output + 'WriCLE_informal')

	for directory in ['WriCLE_formal/', 'WriCLE_informal/']:
		if not os.path.exists(output + directory + 'Spanish'):
			os.system('mkdir ' + output + directory + 'Spanish')

		idx = 1

		for file in os.listdir(path + directory):
			lg = ''

			with io.open(path + directory + file) as f:
				for line in f:
					if line.startswith('Native Language: '):
						lg = line.strip().split(': ')

			if len(lg) > 1 and ' and ' not in lg:
				
				f = io.open(path + directory + file).read()
				try:
					f = f.split('Essay: ')[1].split('\n')
				except:
					f = f.split('Essay:')[1].split('\n')

				essay = []

				for tok in f:
					if len(tok) != 0:
						essay.append(tok)

				new_essay = sentence_split(essay)

				with io.open(output + directory + 'Spanish' + '/' + str(idx) + '.txt', 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')

				idx += 1



### Read text files from TOEFL ###

def read_toefl(path, output):

	if not os.path.exists(output + 'TOEFL'):
		os.system('mkdir ' + output + 'TOEFL')

	for directory in os.listdir(path + 'TOEFL/'):
		lg = directory

		if not os.path.exists(output + 'TOEFL/' + directory):
			os.system('mkdir ' + output + 'TOEFL/' + directory)

		for file in os.listdir(path + 'TOEFL/' + directory):
			if os.stat(path + 'TOEFL/' + directory + '/' + file).st_size != 0:
				essay = []

				with io.open(path + 'TOEFL/' + directory + '/' + file) as f:
					for line in f:
						essay.append(line.strip())

				new_essay = sentence_split(essay) 
				
				with io.open(output + 'TOEFL/' + directory + '/' + file, 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')


### Read EFCAMDAT_data.csv ###

def read_efcamdat(path, output):

	lg_directory = {"cn": 'Chinese', "tr": 'Turkish', "mx": 'Spanish', "fr": 'French', "de": 'German', "br": 'Portuguese', "ru": 'Russian', "sa": 'Arabic', "it": 'Italian', "tw": 'Taiwanese', "jp": 'Japanese'}

	essays = {}

	data = pd.read_csv(path + 'EFCAMDAT_data.csv', encoding = 'utf-8')
	print('Read data')
	L1 = data['nationality'].tolist()
	texts = data['text'].tolist()
	
	for i in range(len(L1)):
		lg = L1[i]
		text = texts[i]
		if lg not in essays:
			essays[lg] = [text]
		else:
			essays[lg].append(text)

	if not os.path.exists(output + 'EFCAMDAT/'):
		os.system('mkdir ' + output + 'EFCAMDAT/')

	idx = 1

	for k, v in essays.items():
		if not os.path.exists(output + 'EFCAMDAT/' + lg_directory[k]):
			os.system('mkdir ' + output + 'EFCAMDAT/' + lg_directory[k])
			print(output + 'EFCAMDAT/' + lg_directory[k])

		for essay in v:
			new_essay = sentence_split(essay)

			with io.open(output + 'EFCAMDAT/' + lg_directory[k] + '/' + str(idx) + '.txt', 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')

			idx += 1


### Read CroLTeC

def read_croltec(path, output):

	lg_directory = {'ara': 'Arabic', 'zh0': 'Chinese', 'zsm': 'Malay', 'nld': 'Dutch', 'zho': 'Chinese', 'afr': 'Afrikaans', 'ltz': 'Luxembourgish', 'ind': 'Indonesian', 'tha': 'Thai', 'som': 'Somali', 'tuk': 'Turkmen', 'ita': 'Italian', 'hun': 'Hungarian', 'vie': 'Vietnamese', 'pol': 'Polish', 'bos': 'Bosnian', 'sqi': 'Albanian', 'bul': 'Bulgarian', 'tur': 'Turkish', 'lug': 'Luganda', 'rus': 'Russian', 'fas': 'Persian', 'isl': 'Icelandic', 'nor': 'Norwegian', 'arc': 'Aramaic', 'fin': 'Finnish', 'ukr': 'Ukrainian', 'mkd': 'Macedonian', 'lrl': 'Lari', 'deu': 'German', 'swe': 'Swedish', 'dan': 'Danish', 'eng': 'English', 'ces': 'Czech', 'est': 'Estonian', 'amh': 'Amharic', 'por': 'Portuguese', 'hin': 'Hindi', 'ron': 'Romainian', 'cat': 'Catalan', 'spa': 'Spanish', 'kor': 'Korean', 'fra': 'French', 'heb': 'Hebrew', 'jpn': 'Japanese', 'mnk': 'Mandinka', 'slv': 'Slovenian', 'slk': 'Slovak'}

	if not os.path.exists(output + 'CroLTeC/'):
		os.system('mkdir ' + output + 'CroLTeC/')

	for lg_code, lg in lg_directory.items():
		if not os.path.exists(output + 'CroLTeC/' + lg):
			os.system('mkdir ' + output + 'CroLTeC/' + lg)

	for xml_file in os.listdir(path + 'CroLTeC/'):
		if xml_file.endswith('.xml'):
			lg_code = xml_file.split('2F')[1][ : 3]
			lg = lg_directory[lg_code]

			file_name = xml_file.split('2F')[1].split('.')[0] + '.txt'

			data = []
			with open(path + 'CroLTeC/' + xml_file) as f:
				for line in f:
					tok = line.strip()
					if '<tok id' in tok:
						data.append(tok)

			new_data = []
			for tok in data:
				tok = tok.split('</tok>')
				if len(tok) > 0:
					for word_info in tok:
						if '<tok id' in word_info:
							word = word_info.split('lemma')
							if len(word) > 1:
								word = word[1].split('>')
								if len(word) > 1:
									word = word[1]
									if '\ufeff' in word:
										word = word.split('\ufeff')[1]
										if word != '':
											new_data.append(word)
									else:
										new_data.append(word)
		
			if len(new_data) != 0:
				with io.open(output + 'CroLTeC/' + lg + '/' + file_name, 'w') as f:
					essay = [' '.join(w for w in new_data)]
					new_essay = sentence_split(essay)
					for sent in new_essay:
						f.write(sent + '\n')


### Read Cople ###

def read_cople(path, output):

	lg_directory = {'ar': 'Arabic', 'de': 'German', 'en': 'English', 'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'nl': 'Dutch', 'pl': 'Polish', 'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'te': 'Tetum', 'zh': 'Chinese'}

	if not os.path.exists(output + 'Cople'):
		os.system('mkdir ' + output + 'Cople')

	for file in os.listdir(path + 'NLI_PT_v2.0/cople/clean/'):
		lg_code = file[ : 2]
		lg = lg_directory[lg_code]

		if not os.path.exists(output + 'Cople/' + lg):
			os.system('mkdir ' + output + 'Cople/' + lg)

		if os.stat(path + 'NLI_PT_v2.0/cople/clean/' + file).st_size != 0:
			essay = []

			with io.open(path + 'NLI_PT_v2.0/cople/clean/' + file) as f:
				for line in f:
					essay.append(line.strip())

			new_essay = sentence_split(essay)
				
			with io.open(output + 'Cople/' + lg + '/' + file, 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')


### Read Leiria ###

def read_leiria(path, output):

	lg_directory = {'eng': 'English', 'french': 'French', 'german': 'German', 'ita': 'Italian', 'kore': 'Korean', 'polish': 'Polish', 'roman': 'Romanian', 'russ': 'Russian', 'span': 'Spanish', 'swed': 'Swedish'}

	if not os.path.exists(output + 'Leiria'):
		os.system('mkdir ' + output + 'Leiria')

	for file in os.listdir(path + 'NLI_PT_v2.0/Leiria/clean/'):
		lg_code = file.split('_')[0]
		lg = lg_directory[lg_code]

		if not os.path.exists(output + 'Leiria/' + lg):
			os.system('mkdir ' + output + 'Leiria/' + lg)

		if os.stat(path + 'NLI_PT_v2.0/Leiria/clean/' + file).st_size != 0:
			essay = []

			with io.open(path + 'NLI_PT_v2.0/Leiria/clean/' + file) as f:
				for line in f:
					essay.append(line.strip())

			new_essay = sentence_split(essay)
				
			with io.open(output + 'Leiria/' + lg + '/' + file, 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')


### Read PEAPLE ###

def read_peaple(path, output):

	lg_directory = {'ALEM': 'German', 'ARABE': 'Arabic', 'CHIN': 'Chinese', 'COREANO': 'Korean', 'ESPANHOL': 'Spanish', 'FRANC': 'French', 'INGL': 'English', 'ITALIANO': 'Italian', 'JAPON': 'Japanese', 'NEERLAND': 'Dutch', 'POLACO': 'Polish', 'ROMENO': 'Romanian', 'RUSSO': 'Russian', 'Tetum': 'Tetum', 'SUECO': 'Swedish'}
	if not os.path.exists(output + 'PEAPLE'):
		os.system('mkdir ' + output + 'PEAPLE')

	for file in os.listdir(path + 'NLI_PT_v2.0/PEAPLE2/clean/'):
		lg_code = ''
		if file.startswith('ALEM'):
			lg_code = 'ALEM'		
		if file.startswith('ARABE'):
			lg_code = 'ARABE'
		if file.startswith('CHIN'):
			lg_code = 'CHIN'
		if file.startswith('COREANO'):
			lg_code = 'COREANO'
		if file.startswith('ESPANHOL'):
			lg_code = 'ESPANHOL'
		if file.startswith('FRANC'):
			lg_code = 'FRANC'
		if file.startswith('INGL'):
			lg_code = 'INGL'
		if file.startswith('ITALIANO'):
			lg_code = 'ITALIANO'
		if file.startswith('JAPON'):
			lg_code = 'JAPON'
		if file.startswith('NEERLAND'):
			lg_code = 'NEERLAND' 
		if file.startswith('POLACO'):
			lg_code = 'POLACO' 
		if file.startswith('ROMENO'):
			lg_code = 'ROMENO' 
		if file.startswith('RUSSO'):
			lg_code = 'RUSSO' 
		if file.startswith('SUECO'):
			lg_code = 'SUECO' 
		if 'TUM' in file: 
			lg_code = 'Tetum'

		lg = lg_directory[lg_code]

		if not os.path.exists(output + 'PEAPLE/' + lg):
			os.system('mkdir ' + output + 'PEAPLE/' + lg)

		if os.stat(path + 'NLI_PT_v2.0/PEAPLE2/clean/' + file).st_size != 0:
			essay = []

			with io.open(path + 'NLI_PT_v2.0/PEAPLE2/clean/' + file) as f:
				for line in f:
					essay.append(line.strip())

			new_essay = sentence_split(essay)
				
			with io.open(output + 'PEAPLE/' + lg + '/' + file, 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')


### Read ICNALE ###

def read_icnale(path, output):

	lg_directory = {'CHN': 'Chinese', 'HKG': 'Cantonese', 'IDN': 'Indonesian', 'JPN': 'Japanese', 'KOR': 'Korean', 'PAK': 'Pakistan', 'PHL': 'Philippines', 'SIN': 'Malay', 'THA': 'Thailand', 'TWN': 'Taiwanese', 'UAE': 'Arabic'}

	if not os.path.exists(output + 'ICNALE'):
		os.system('mkdir ' + output + 'ICNALE')

	for file in os.listdir(path + 'ICNALE_Written_Essays_2.4/Merged/*Text/'):
		lg_code = file.split('_')[1]
		if lg_code in lg_directory:
			lg = lg_directory[lg_code]

			if not os.path.exists(output + 'ICNALE/' + lg):
				os.system('mkdir ' + output + 'ICNALE/' + lg)

			if os.stat(path + 'ICNALE_Written_Essays_2.4/Merged/*Text*/' + file).st_size != 0:
				essay = []

				with io.open(path + 'ICNALE_Written_Essays_2.4/Merged/*Text*/' + file) as f:
					for line in f:
						essay.append(line.strip())

				new_essay = sentence_split(essay)
				
				with io.open(output + 'ICNALE/' + lg + '/' + file, 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')

### Read MERLIN ###

def read_merlin(path, output):

	l2_dict = {'german': 'German', 'czech': 'Czech', 'italian': 'Italian'}

	for l2, L2 in l2_dict.items():
		if not os.path.exists(output + 'MERLIN_' + L2):
			os.system('mkdir ' + output + 'MERLIN_' + L2)

		for file in os.listdir(path + 'merlin-text-v1.1/plain/' + l2 + '/'):
			if file in os.listdir(path + 'merlin-text-v1.1/meta_ltext/' + l2 + '/'):
				with io.open(path + 'merlin-text-v1.1/meta_ltext/' + l2 + '/' + file) as meta_f:
					l1 = ''
					for line in meta_f:
						line = line.strip()
						if line.startswith('Mother tongue') or line.startswith('mother tongue'):
							l1_info = line.split(': ')[1].split()
							if len(l1_info) == 1:
								l1 = l1_info[0]

					if l1 not in ['', 'Other', 'other', 'EMPTY']:
						if not os.path.exists(output + 'MERLIN_' + L2 + '/' + l1):
							os.system('mkdir ' + output + 'MERLIN_' + L2 + '/' + l1)

						essay = []
						with io.open(path + 'merlin-text-v1.1/plain/' + l2 + '/' + file) as f:
							for line in f:
								essay.append(line.strip())

						new_essay = sentence_split(essay)
						with io.open(output + 'MERLIN_' + L2 + '/' + l1 + '/' + file, 'w') as f:
							for sent in new_essay:
								f.write(sent + '\n')



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to resources/')
	parser.add_argument('--output', type = str, help = 'path to data/')
	parser.add_argument('--corpus', type = str, help = 'e.g., pelic, toefl')

	args = parser.parse_args()

	corpus = args.corpus
	function_maps = {'caes': read_caes, 'cows': read_cows, 'cedel': read_cedel, 'pelic': read_pelic, 'wricle': read_wricle, 'pelic': read_pelic, 'toefl': read_toefl, 'efcamdat': read_efcamdat, 'croltec': read_croltec, 'cople': read_cople, 'leiria': read_leiria, 'peaple': read_peaple, 'icnale': read_icnale, 'merlin': read_merlin}

	function_maps[corpus](args.input, args.output)




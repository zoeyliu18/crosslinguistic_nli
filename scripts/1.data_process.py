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

	if not os.path.exists(output + 'CAES'):
		os.system('mkdir ' + output + 'CAES')

	for directory in os.listdir(path + 'CAES/'):
		lg = directory

		if not os.path.exists(output + 'CAES/' + directory):
			os.system('mkdir ' + output + 'CAES/' + directory)

		for file in os.listdir(path + 'CAES/' + directory):
			if os.stat(path + 'CAES/' + directory + '/' + file).st_size != 0:
				essay = []

				with io.open(path + 'CAES/' + directory + '/' + file) as f:
					for line in f:
						essay.append(line.strip())

				new_essay = sentence_split(essay)
				
				with io.open(output + 'CAES/' + directory + '/' + file, 'w') as f:
					for sent in new_essay:
						f.write(sent + '\n')

### Read COWSL2H ###

def read_cows(path, output):

	essays = {}

	for file in os.listdir(path):
		data = pd.read_csv(path + file, encoding = 'utf-8')
		L1 = data['l1 language'].tolist()
		print(L1)
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
		if not os.path.exists(output + 'PELIC/' + k):
			os.system('mkdir ' + output + 'PELIC/' + k)

		for essay in v:
			new_essay = sentence_split(essay)

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

	essays = {}

	data = pd.read_csv(path + 'EFCAMDAT_data.csv', encoding = 'utf-8')
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
		if not os.path.exists(output + 'EFCAMDAT/' + k):
			os.system('mkdir ' + output + 'EFCAMDAT/' + k)

		for essay in v:
			new_essay = sentence_split(essay)

			with io.open(output + 'EFCAMDAT/' + k + '/' + str(idx) + '.txt', 'w') as f:
				for sent in new_essay:
					f.write(sent + '\n')

			idx += 1


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to resources/')
	parser.add_argument('--output', type = str, help = 'path to data/')
	parser.add_argument('--corpus', type = str, help = 'e.g., pelic, toefl')

	args = parser.parse_args()

	corpus = args.corpus
	function_maps = {'caes': read_caes, 'cows': read_cows, 'cedel': read_cedel, 'pelic': read_pelic, 'wricle': read_wricle, 'pelic': read_pelic, 'toefl': read_toefl, 'efcamdat': read_efcamdat}

	function_maps[corpus](args.input, args.output)




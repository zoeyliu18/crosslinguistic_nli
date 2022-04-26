import io, os, argparse

def conll_read_sentence(file_handle):

	sent = []

	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				if toks[0] == 'q1':
					toks[0] = '1'
				sent.append(toks)

	return None

def unigram_pos(file):

	data = []

	with io.open(file) as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			pos_list = []
			for tok in sent:
				data.append(tok[3])

			sent = conll_read_sentence(f)

	return data

def unigram_deprel(file):

	data = []

	with io.open(file) as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			deprel_list = []
			for tok in sent:
				data.append(tok[7])

			sent = conll_read_sentence(f)

	return data


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to processed/')
	parser.add_argument('--output', type = str, help = 'path to results/')
	parser.add_argument('--lg', type = str, help = 'en, es, hr')

	args = parser.parse_args()

	header = ['POS', 'Deprel', 'Lang']

	corpus_list = []

	if args.lg == 'en':
		corpus_list = ['TOEFL', 'WriCLE_formal', 'WriCLE_informal', 'PELIC']
	if args.lg == 'es':
		corpus_list = ['CAES', 'COWS', 'CEDEL']

	for corpus in corpus_list:
		print(corpus)
		output_file = io.open(args.output + corpus + '_syntax.txt', 'w')
		info = []

		for directory in os.listdir(args.input + corpus):
			print(directory)

			lang = directory
			
			txt_c = 0
			conllu_c = 0

			for file in os.listdir(args.input + corpus + '/' + directory):
				if file.endswith('.txt'):
					txt_c += 1

				if file.endswith('.conllu'):
					conllu_c += 1
					pos_data = unigram_pos(args.input + corpus + '/' + directory + '/' + file)
					deprel_data = unigram_deprel(args.input + corpus + '/' + directory + '/' + file)
					pos_data = ' '.join(pos for pos in pos_data)
					deprel_data = ' '.join(deprel for deprel in deprel_data)
					output_file.write(pos_data + '\t' + deprel_data + '\t' + lang + '\n')
			
			if txt_c != conllu_c:
				print('Text and Conllu numbers do not match!')

			if conllu_c == 0:
				print('No Conllu files!')


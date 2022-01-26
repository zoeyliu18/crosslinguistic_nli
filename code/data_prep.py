import io, os, argparse, random

def conll_read_sentence(file_handle):

	sent = []

	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)

	return None

def generate_data(file):

	upos_data = []
	xpos_data = []
	deprel_data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
			sent_upos = []
			sent_xpos = []
			sent_deprel = []
		
			for tok in sent:
				if tok[7] != 'punct':
					sent_upos.append(tok[3])
					sent_xpos.append(tok[4])
					sent_deprel.append(tok[7])
				else:
					sent_upos.append(tok[1])
					sent_xpos.append(tok[1])
					sent_deprel.append(tok[1])
				#	print(sent_upos)

			upos_data.append(' '.join(pos for pos in sent_upos))
			xpos_data.append(' '.join(pos for pos in sent_xpos))
			deprel_data.append(' '.join(deprel for deprel in sent_deprel))

			sent = conll_read_sentence(f)

	return upos_data, xpos_data, deprel_data


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to TOEFL data')
	parser.add_argument('--output', type = str, help = 'output training/test file')

	args = parser.parse_args()

	all_labels = []
	all_upos_data = []
	all_xpos_data = []
	all_deprel_data = []

	for folder in os.listdir(args.input):
		if os.path.isdir(args.input + folder) is True:
			lang = folder
			for file in os.listdir(args.input + folder + '/'):
				if file.endswith('.conllu'):
					upos_data, xpos_data, deprel_data = generate_data(args.input + folder + '/' + file)
					if upos_data == []:
						print(file, folder)
					all_upos_data.append(' '.join(sent for sent in upos_data))
					all_xpos_data.append(' '.join(sent for sent in xpos_data))
					all_deprel_data.append(' '.join(sent for sent in deprel_data))
					all_labels.append(lang)

	assert len(all_labels) == len(all_xpos_data)

	index_list = []

	for i in range(len(all_labels)):
		index_list.append(i)

	for z in range(1, 2):

		random.shuffle(index_list)

		train_upos_data = []
		test_upos_data = []
		train_xpos_data = []
		test_xpos_data = []
		train_deprel_data = []
		test_deprel_data = []
		train_labels = []
		test_labels = []

		for i in range(0, int(len(index_list) * 0.8)):
			idx = index_list[i]
			train_upos_data.append(all_upos_data[i] + ' ' + all_labels[i])
			train_xpos_data.append(all_xpos_data[i] + ' ' + all_labels[i])
			train_deprel_data.append(all_deprel_data[i] + ' ' + all_labels[i])
		#	train_labels.append(all_labels[i].append(all_labels[i]))

		for i in range(int(len(index_list) * 0.8), len(index_list)):
			idx = index_list[i]
			test_upos_data.append(all_upos_data[i] + ' ' + all_labels[i])
			test_xpos_data.append(all_xpos_data[i] + ' ' + all_labels[i])
			test_deprel_data.append(all_deprel_data[i] + ' ' + all_labels[i])
		#	test_labels.append(all_labels[i])

		with io.open(args.output + 'toefl_upos_train' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in train_upos_data:
				f.write(tok + '\n')

		with io.open(args.output + 'toefl_upos_test' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in test_upos_data:
				f.write(tok + '\n')

		with io.open(args.output + 'toefl_xpos_train' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in train_xpos_data:
				f.write(tok + '\n')

		with io.open(args.output + 'toefl_xpos_test' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in test_xpos_data:
				f.write(tok + '\n')

		with io.open(args.output + 'toefl_deprel_train' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in train_deprel_data:
				f.write(tok + '\n')

		with io.open(args.output + 'toefl_deprel_test' + str(z) + '.txt', 'w', encoding = 'utf-8') as f:
			for tok in test_deprel_data:
				f.write(tok + '\n')








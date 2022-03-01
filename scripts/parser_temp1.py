#usr/bin/env python3

import io, os, argparse
from diaparser.parsers import Parser
import pandas as pd
import stanza

en_nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
es_nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma,depparse')
hr_nlp = stanza.Pipeline(lang='hr', processors='tokenize,pos,lemma,depparse')

### Read each essay in individual *.txt format ###

def read_essay(file, path):

	essay = []

	with io.open(path + file, encoding = 'utf-8') as f:
		for line in f:
			toks = line.strip().split()
			essay.append(toks)

	return essay


### Getting POS and STEM features from Stanza ###

def get_features(sentence, lg, l1):

	tokens = []
	for tok in sentence:
		tokens.append(tok[1])

	utterance = ' '.join(w for w in tokens)

	parse_info = ''
	if lg == 'en':
		parse_info = en_nlp(utterance)
	if lg == 'es':
		parse_info = es_nlp(utterance)
	if lg == 'hr':
		parse_info = hr_nlp(utterance)

	parse_results = []

	for sent in parse_info.sentences:
		for i in range(len(sent.words)):
			word = sent.words[i]
			w_id = word.id
			w_text = word.text
			w_lemma = word.lemma
			w_upos = word.upos
			w_xpos = word.xpos
			w_feats = word.feats
			w_head = word.head
			w_deprel = word.deprel
			parse_results.append([w_id, w_text, w_lemma, w_upos, w_xpos, w_feats, w_head, w_deprel, lg, l1])

	return parse_results


### Predict parses of sentences from a file with a trained model ###

def predict(file, path, model, lg, l1):

	predictions = []

	data = read_essay(file, path)

	if os.stat(path + file).st_size != 0:
		for sent in data:
			pred = model.predict([sent], prob = True)
			pred_values = pred.sentences[0].values

	# values format	
	# [('1', '2', '3', '4', '5'), ('She', 'enjoys', 'playing', 'tennis', '.'), ('_', '_', '_', '_', '_'), ('_', '_', '_', '_', '_'), ('_', '_', '_', '_', '_'), ('_', '_', '_', '_', '_'), [2, 3, 0, 3, 3], ['nsubj', 'aux', 'root', 'obj', 'obj'], ('_', '_', '_', '_', '_'), ('_', '_', '_', '_', '_')]

			info = []
			for i in range(len(pred_values[0])):
				word_info = []
				for z in range(len(pred_values)):
					word_info.append(pred_values[z][i])
				info.append(word_info)

			predictions.append(info)
	
		file_name = file.split('.')[0]

		with io.open(path + file_name + '.conllu', 'w') as f:
			for sent in predictions:
				sent_feats = get_features(sent, lg, l1)
				for tok in sent_feats:
					f.write('\t'.join(str(w) for w in tok) + '\n')
				f.write('\n')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to data/')
	parser.add_argument('--lg', type = str, help = 'en, es, hr')

	args = parser.parse_args()

	if args.lg == 'en':
		model = Parser.load('models/en_ewt_model')
		for corpus in ['WriCLE_informal', 'PELIC']:
			print(corpus)
			for directory in os.listdir(args.input + corpus):
				if directory in ['Spanish, Arabic, Thai, Taiwanese, French']:
					for file in os.listdir(args.input + corpus + '/' + directory):
						file_name = file.split('.')[0]
						check = 0
						with io.open(args.input + corpus + '/' + directory + '/' + file_name + '.conllu') as f:
							for line in f:
								toks = line.split('\t')
								if 'None' in toks:
									check += 1
									break
						if check != 0:
							try:
								print(file)
								predict(file, args.input + corpus + '/' + directory + '/', model, 'en', directory)
							except:
								pass
					#	if file_name + '.conllu' not in os.listdir(args.input + corpus + '/' + directory + '/') or os.stat(args.input + corpus + '/' + directory + '/' + file_name + '.conllu').st_size == 0:	
					#		print(file)
					#		try:
					#			predict(file, args.input + corpus + '/' + directory + '/', model, 'en', directory)
					#		except:
					#			pass
							
	if args.lg == 'es':
		model = Parser.load('models/es_ancora_model')
		for corpus in ['CEDEL']:
			print(corpus)
			for directory in os.listdir(args.input + corpus):
				print(directory)
				for file in os.listdir(args.input + corpus + '/' + directory):
					file_name = file.split('.')[0]
					if file_name + '.conllu' not in os.listdir(args.input + corpus + '/' + directory + '/') or os.stat(args.input + corpus + '/' + directory + '/' + file_name + '.conllu').st_size == 0:	
						try:
							predict(file, args.input + corpus + '/' + directory + '/', model, 'es', directory)
						except:
							pass


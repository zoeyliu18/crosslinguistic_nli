#usr/bin/env python3

import io, os, argparse
from machamp.parsers import Parser
import pandas as pd
import stanza


### Read each essay in individual *.txt format ###

def read_essay(file, path):

	essay = []

	with io.open(path + file, encoding = 'utf-8') as f:
		for line in f:
			toks = line.strip().split()
			if toks != []:
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
		en_nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
		parse_info = en_nlp(utterance)
	if lg == 'es':
		es_nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma,depparse')
		parse_info = es_nlp(utterance)
	if lg == 'hr':
		hr_nlp = stanza.Pipeline(lang='hr', processors='tokenize,pos,lemma,depparse')
		parse_info = hr_nlp(utterance)
	if lg == 'pt':
		pt_nlp = stanza.Pipeline(lang='pt', processors='tokenize,pos,lemma,depparse')
		parse_info = pt_nlp(utterance)
	if lg == 'cs':
		cs_nlp = stanza.Pipeline(lang='cs', processors='tokenize,pos,lemma,depparse')
		parse_info = cs_nlp(utterance)

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

def predict(file, path, output, model, lg, l1):

	predictions = []

	if os.stat(path + file).st_size != 0:
		data = read_essay(file, path)
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

		with io.open(output + file_name + '.conllu', 'w') as f:
			for sent in predictions:
				sent_feats = get_features(sent, lg, l1)
				for tok in sent_feats:
					f.write('\t'.join(str(w) for w in tok) + '\n')
				f.write('\n')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--lg', type = str, help = 'en, es, hr')
	parser.add_argument('--corpus', type = str, help = 'e.g., PELIC, TOEFL')
	parser.add_argument('--emb', type = str, help = 'e.g., mbert or xlmr')
	parser.add_argument('--seed', default = '1', help = 'e.g., 1, 2, 3')
	args = parser.parse_args()

	corpus = args.corpus
	emb = args.emb
	seed = args.seed 

	model = ''
	lg_code = ''

	if args.lg == 'en':
		lg_code = 'en_ewt'

	if args.lg == 'es':
		lg_code = 'es_ancora'

	if args.lg == 'hr':
		lg_code = 'hr_set'

	if args.lg == 'pt':
		lg_code = 'pt_gsd'

	if args.lg == 'cs':
		lg_code = 'cs_pdt'

	if not os.path.exists('parses/'):
		os.system('mkdir parses/')

	if not os.path.exists('parses/' + corpus):
		os.system('mkdir ' + 'parses/' + corpus)

	for directory in os.listdir('data/' + corpus):
		if os.path.isdir('data/' + corpus + '/' + directory):
			if not os.path.exists('parses/' + corpus + '/' + directory):
				os.system('mkdir ' + 'parses/' + corpus + '/' + directory)

			if not os.path.exists('parses/' + corpus + '/' + directory + '/machamp' + '_' + emb + '_' + seed):
				os.system('mkdir ' + 'parses/' + corpus + '/' + directory + '/machamp' + '_' + emb + '_' + seed)

			if len(os.listdir('data/' + corpus + '/' + directory)) != 0:
				for file in os.listdir('data/' + corpus + '/' + directory):
					file_name = file.split('.')[0]
					if file_name + '.conllu' not in os.listdir('parses/' + corpus + '/' + directory + '/machamp' + '_' + emb + '_' + seed) or os.stat('parses/' + corpus + '/' + directory + '/machamp' + '_' + emb + '_' + seed + '/' + file_name + '.conllu').st_size == 0:	
						try:
							os.system("python3 predict.py logs/models/" + lg_code + '/' + emb + '_' + seed + '/*/model.tar.gz data/' + corpus + '/' + directory + '/' + file + ' parses/' + corpus + '/' + directory + '/machamp' + '_' + emb + '_' + seed + '/' + file_name + '.conllu --device 0')
						except:
							pass 


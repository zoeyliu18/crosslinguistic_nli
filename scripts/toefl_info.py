### This scripts process TOEFL data sets to CoNLL formats with POS tags and dependency relations ###
### 12,100 essays ###
### ====  ======== ###
### Code  Language ### 
### ====  ======== ### 
### ARA   Arabic ### 
### DEU   German ### 
### FRA   French ### 
### HIN   Hindi ### 
### ITA   Italian ### 
### JPN   Japanese ### 
### KOR   Korean ### 
### SPA   Spanish ### 
### TEL   Telugu ### 
### TUR   Turkish ### 
### ZHO   Chinese ### 
### ====  ======== ### 

import io, os, string, argparse
from diaparser.parsers import Parser
import pandas as pd
import stanza

language_maps = {'ARA': 'ar', 'DEU': 'de', 'FRA': 'fr', 'HIN': 'hi', 'ITA': 'it', 'JPN': 'ja', 'KOR': 'ko', 'SPA': 'es', 'TEL': 'te', 'TUR': 'tr', 'ZHO': 'zh'}

en_parser = Parser.load('en_ewt-electra')

nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True)

### Read index information ###

def read_index(path):

	index = pd.read_csv(path + 'index.csv', encoding = 'utf-8')
	information = {}

	filenames = index['Filename'].tolist()
	prompts = index['Prompt'].tolist()
	languages = index['Language'].tolist()
	levels = index['Score Level'].tolist()
	
	for k, v in language_maps.items():
		if k not in information:
			information[k] = {}

		for i in range(len(filenames)):
			
			if languages[i] == k:
				information[k][filenames[i]] = [prompts[i], languages[i], levels[i]]

	return information


### Read each essay ###

def read_essay(file, path):

	essay = []

	with io.open(path + file, encoding = 'utf-8') as f:
		for line in f:
			toks = line.strip()
			essay.append(toks)

	return essay


### Getting POS and STEM features from Stanza ###

def get_features(sentence, lang, file, promt, level):

	tokens = []
	for tok in sentence:
		tokens.append(tok[1])

	utterance = ' '.join(w for w in tokens)

	parse_info = nlp(utterance)

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
			w_head = sentence[i][6]
			w_deprel = sentence[i][7]

			parse_results.append([w_id, w_text, w_lemma, w_upos, w_xpos, w_feats, w_head, w_deprel, language_maps[lang], file + ' ' + promt + ' ' + level])

	return parse_results


def parse(sentence, lang, file, promt, level):

	temp_parse_results = []

	parse_tree = ''

	try:
		parse_tree = en_parser.predict(sentence, text = 'en').sentences[0]
		attributes = parse_tree.__dict__['values']
		for k in range(len(attributes[0])):
			feature = []
			for z in attributes:
				feature.append(str(z[k]))

			temp_parse_results.append(feature)

	except:
		print(sentence)
	
#	attributes[2] = tuple(new_stem_list[i])
#	attributes[3] = tuple(new_pos_list[i])
#	attributes[-2] = tuple([speaker_feature[i]] * len(attributes[0]))
#	attributes[-1] = tuple([child_feature[i]] * len(attributes[0]))

	if temp_parse_results != []:
		parse_results = get_features(temp_parse_results, lang, file, promt, level)

		return parse_results

	return None


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to TOEFL data')
	parser.add_argument('--output', type = str, help = 'output .conllu file')

	args = parser.parse_args()

	index_information = read_index(args.input)

	for lang, files in index_information.items():
		print(lang)
		if not os.path.exists(args.output + language_maps[lang] + '/'):
			os.makedirs(args.output + language_maps[lang] + '/')

#		for file in os.listdir(args.input + 'responses/tokenized/'):
#			if file in files:
#				os.system('cp ' + args.input + 'responses/tokenized/' + file + ' ' + args.output + language_maps[lang] + '/')

	for lang, files in index_information.items():
		for file in os.listdir(args.output + language_maps[lang] + '/'):
			if file.endswith('.txt'):
				file_id = file.split('.')[0]

			#	if file_id + '.conllu' not in os.listdir(args.output + language_maps[lang] + '/'):
			#	if language_maps[lang] == 'ar': # and file_id == '476899':
				if file_id in ['1574990', '12130', '125348', '1483561']:
					print(file_id)
					with io.open(args.output + language_maps[lang] + '/' + file_id + '.conllu', 'w', encoding = 'utf-8') as f:
						promt = files[file][0]
						level = files[file][-1]

						essay = read_essay(file, args.input + 'responses/tokenized/')
						essay_conll = []

						for sent in essay:
							sent_parse = parse(sent, lang, file, promt, level)

							if sent_parse is not None:

								f.write('# text = ' + ' '.join(str(tok[1]) for tok in sent_parse) + '\nq')

								for tok in sent_parse:
									f.write('\t'.join(str(w) for w in tok) + '\n')

								f.write('\n')





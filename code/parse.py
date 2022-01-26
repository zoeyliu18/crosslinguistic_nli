import io, os, string, argparse
from diaparser.parsers import Parser
import pandas as pd
import stanza

en_language_maps = {'ARA': 'ar', 'DEU': 'de', 'FRA': 'fr', 'HIN': 'hi', 'ITA': 'it', 'JPN': 'ja', 'KOR': 'ko', 'SPA': 'es', 'TEL': 'te', 'TUR': 'tr', 'ZHO': 'zh'}

en_parser = Parser.load('en_ewt-electra')

en_nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True)

es_parser = Parser.load('es_ancora.mbert')

es_nlp = stanza.Pipeline(lang='es', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True)

es_language_maps = {'Arabe': 'ar', 'Chino_mandarin': 'zh', 'Frances': 'fr', 'Ingles': 'en', 'Portugues': 'pt', 'Ruso': 'ru'}

### Read each essay ###

def read_essay(file):

	essay = []

	with io.open(file, encoding = 'utf-8') as f:
		for line in f:
			toks = line.strip()
			essay.append(toks)

	return essay


### Getting POS and STEM features from Stanza ###

def get_features(sentence, lang, language_maps):

	tokens = []
	for tok in sentence:
		tokens.append(tok[1])

	utterance = ' '.join(w for w in tokens)

	parse_info = ''
	if language_maps == en_language_maps:
		parse_info = en_nlp(utterance)
	if language_maps == es_language_maps:
		parse_info = es_nlp(utterance)

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
			parse_results.append([w_id, w_text, w_lemma, w_upos, w_xpos, w_feats, w_head, w_deprel, language_maps[lang], ''])

	return parse_results


def parse(sentence, lang, language_maps):

	temp_parse_results = []

	parse_tree = ''

	try:
		parse_tree = es_parser.predict(sentence, text = 'es').sentences[0]
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
		parse_results = get_features(temp_parse_results, lang, language_maps)

		return parse_results

	return None


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to *.txt data')
	parser.add_argument('--lang', type = str, help = 'language')

	args = parser.parse_args()

	language_maps = ''
	if args.lang == 'en':
		language_maps = en_language_maps
	if args.lang == 'es':
		language_maps = es_language_maps

	for directory in os.listdir(args.input):
		if os.path.isdir(args.input + directory + '/'):
			lang = directory
			print(lang)
			for file in os.listdir(args.input + directory + '/'):
				if file.endswith('txt'):
					file_id = file.split('.')[0]

					if file_id + '.conllu' not in os.listdir(args.input + directory + '/') or os.stat(args.input + directory + '/' + file_id + '.conllu').st_size == 0:
				#	if 2 > 1:
						print(lang, file_id)
						with io.open(args.input + directory + '/' + file_id + '.conllu', 'w', encoding = 'utf-8') as f:

							essay = read_essay(args.input + directory + '/' + file)
							essay_conll = []

							for sent in essay:
								sent_parse = parse(sent, lang, language_maps)

								if sent_parse is not None:

									f.write('# text = ' + ' '.join(str(tok[1]) for tok in sent_parse) + '\nq')

									for tok in sent_parse:
										f.write('\t'.join(str(w) for w in tok) + '\n')

									f.write('\n')





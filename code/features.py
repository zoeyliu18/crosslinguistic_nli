### This script calculates dependency-tree based linguistic features for *.conllu files ###

import io, os, argparse, random, statistics, math
import networkx as nx

function_POS = ['ADP', 'AUX', 'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ']
clauses = ['csubj', 'ccomp', 'xcomp', 'advcl', 'acl']
verb_features = ['Mood', 'Number', 'Person', 'Tense', 'VerbForm']

verb_mood_features = ['Ind', 'Imp', 'Cnd', 'Pot', 'Sub', 'Jus', 'Prp', 'Qot', 'Opt', 'Des', 'Nec', 'Irr', 'Adm']
verb_number_features = ['Sing', 'Plur', 'Dual', 'Tri', 'Pau', 'Grpa', 'Grpl', 'Inv', 'Count', 'Ptan', 'Coll']
verb_tense_features = ['Past', 'Pres', 'Fut', 'Imp', 'Pqp']
verb_aspect_features = ['Imp', 'Perf', 'Prosp', 'Prog', 'Hab', 'Iter']
verb_voice_features = ['Act', 'Mid', 'Rcp', 'Pass', 'Antip', 'Lfoc', 'Bfoc', 'Dir', 'Inv', 'Cau']
verb_evident_features = ['Fh', 'Nfh']
verb_form_features = ['Fin', 'Inf', 'Sup', 'Part', 'Conv', 'Gdv', 'Ger', 'Vnoun']
verb_polarity_features = ['Pos', 'Neg']
verb_person_features = ['0', '1', '2', '3', '4']
verb_polite_features = ['Infm', 'Form', 'Elev', 'Humb']
verb_clusivity_features = ['In', 'Ex']

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

def distribution(data_list):

	if len(set(data_list)) > 1:
		unique = set(data_list)
		prob_list = []
		H = 0

		for tok in unique:
			prob = data_list.count(tok) / len(data_list)
			prob_list.append(prob)
			H += -1 * (prob * math.log2(prob))

		std = statistics.stdev(prob_list)
		value_range = max(prob_list) - min(prob_list)
		return H, std, value_range

	if len(set(data_list)) == 1:
		return 0, '', ''

	if len(set(data_list)) == 0:
		return '', '', ''

def has_subj(verb_index, sent):

	subj = ''

	for tok in sent:
		if tok[7] == 'nsubj' and tok[6] == verb_index:
			subj = tok
			return subj

	return None

def has_obj(verb_index, sent):

	obj = ''

	for tok in sent:
		if tok[7] == 'obj' and tok[6] == verb_index:
			obj = tok
			return obj

	return None

def has_iobj(verb_index, sent):

	iobj = ''

	for tok in sent:
		if tok[7] == 'iobj' and tok[6] == verb_index:
			iobj = tok
			return iobj

	return None

def word_order(verb_index, sent):
	order = []

	subj = has_subj(verb_index, sent)
	obj = has_obj(verb_index, sent)
	iobj = has_iobj(verb_index, sent)

	deprel_map = {'nsubj': 's', 'obj': 'o', 'iobj': 'io', 'VERB': 'v'}

	core_list = [int(verb_index)]
	if subj is not None:
		core_list.append(int(subj[0]))
	if obj is not None:
		core_list.append(int(obj[0]))
	if iobj is not None:
		core_list.append(int(iobj[0]))

	core_list.sort()
	for i in range(len(core_list)):
		idx = core_list[i]
		tok = sent[idx - 1]
		if tok[0] == verb_index:
			order.append('v')
		else:
			order.append(deprel_map[tok[7]])

	return order

def has_surbodinate(verb_index, sent):

	subordinate = []

	for tok in sent:
		if tok[7] in clauses and tok[6] == verb_index:
			subordinate.append(tok)

	return subordinate

### Get the syntactic dependents of a token ###

def dependents(index, sentence):

	dependent = []

	for tok in sentence:
		if tok[6] == index:
			dependent.append(tok[0])

	if len(dependent) != 0:
		return dependent

	return None

####### Get the subtree of a syntactic head ######

def subtree_generate(index, sentence):

	idxlist = [index]
	min_idx = len(sentence)
	max_idx = 0

	while len(idxlist) != 0:
		i = idxlist.pop()
	
		if int(i) < min_idx:
			min_idx = int(i)
	
		if int(i) > max_idx:
			max_idx = int(i)
	
		i_d = dependents(i, sentence)
	
		if i_d is not None:
			for d in i_d:
				idxlist.append(d)

	subtree = sentence[min_idx - 1 : max_idx]

	subtree_idx = []

	for idx in range(min_idx - 1, max_idx):
		subtree_idx.append(int(idx))

	subtree_idx.sort() 

	return subtree, subtree_idx

def verbal_inflection(index, sentence):
	tok = sentence[int(index) - 1]
	features = tok[5]
	mood_feature = ''
	number_feature = ''
	person_feature = ''
	tense_feature = ''
	form_feature = ''
	aspect_feature = ''
	voice_feature = ''
	evident_feature = ''
	polarity_feature = ''
	polite_feature = ''
	clusivity_feature = ''

	if features != 'None':
		verbal_features = features.split('|')
		for feature in verbal_features:
			if feature.startswith('Mood'):
				mood_feature = feature.split('=')[1]
			if feature.startswith('Number'):
				number_feature = feature.split('=')[1]
			if feature.startswith('Person'):
				person_feature = feature.split('=')[1]
			if feature.startswith('Tense'):
				tense_feature = feature.split('=')[1]
			if feature.startswith('VerbForm'):
				form_feature = feature.split('=')[1]
			if feature.startswith('Aspect'):
				aspect_feature = feature.split('=')[1]
			if feature.startswith('Voice'):
				voice_feature = feature.split('=')[1]
			if feature.startswith('Evident'):
				evident_feature = feature.split('=')[1]
			if feature.startswith('Polariy'):
				polarity_feature = feature.split('=')[1]
			if feature.startswith('Polite'):
				polite_feature = feature.split('=')[1]
			if feature.startswith('Clusivity'):
				clusivity_feature = feature.split('=')[1]

	return mood_feature, number_feature, person_feature, tense_feature, form_feature, aspect_feature, voice_feature, evident_feature, polarity_feature, polite_feature, clusivity_feature

def dictionary_ratio(dictionary):

	total = 0
	for k, v in dictionary.items():
		total += v 

	if total != 0:
		for k, v in dictionary.items():
			dictionary[k] = v / total

	return dictionary


def analyze(g):
	np_words = set()
	doms = {}
	
	# for each node in g, get list of dominating nodes
	for node in g:
		doms[node] = nx.shortest_path(g, source = 0, target = node)

	# for each edge (u,v) in g, determine whether all intervening words (ids) are dominated by u
	for edge in g.edges():
		u = edge[0]
		v = edge[1]
		i = 1
		if u > v:
			i = -1
		for n in range(u+i,v,i):
			if u not in doms[n]:
				np_words.add(n)

	n = len(np_words)

	# for calculating dependency tree depth
	len_list = []

	for k, v in doms.items():
		len_list.append(len(v))

	len_list = list(set(len_list))
	temp_max_depth = max(len_list)

	if temp_max_depth == 2:
		max_depth = 1
	else:
		max_depth = temp_max_depth - 2

	# return whether this tree has a non-projective dependency and number of non-projective words (ids)
	return int(n > 0), n, max_depth

### Analyze a *.conllu file ###

def full_analyze(file_handle):
	num_sent = 0

	num_word = 0
	num_word_type = 0
	content_word = 0
	content_word_type = 0
	function_word = 0
	function_word_type = 0
	lexical_density = 0

	word_list = []
	word_len_list = []
	function_word_list = []
	function_lemma_list = []

	num_lemma_type = 0
	lemma_list = []
	lemma_len_list = []

	num_pos_type = 0
	pos_list = []

	ttr_word = 0
	ttr_lemma = 0

	ave_sent_len = 0
	ave_word_len = 0

	verb_word_list = []
	verb_lemma_list = []
	verb_mood_list = []
	verb_number_list = []
	verb_person_list = []
	verb_tense_list = []
	verb_form_list = []
	verb_aspect_list = []
	verb_voice_list = []
	verb_evident_list = []
	verb_polarity_list = []
	verb_polite_list = []
	verb_clusivity_list = []

	verb_valency_list = []

	aux_word_list = []
	aux_lemma_list = []
	aux_mood_list = []
	aux_number_list = []
	aux_person_list = []
	aux_tense_list = []
	aux_form_list = []
	aux_aspect_list = []
	aux_voice_list = []
	aux_evident_list = []
	aux_polarity_list = []
	aux_polite_list = []
	aux_clusivity_list = []

	deprel_list = []

	subordinate_deprel_list = []
	subordinate_depth_list = []
	subordinate_order_list = []

	deplen_list = []
	headedness_list = []

	clause_len_list = []
	verb_valency_list = []
	word_order_list = []

	word_order_dictionary = {'s_v': 0, 'v_s': 0, 'v_o': 0, 'o_v': 0}
	subordinate_order_dictionary = {'subordinate_head_initial': 0, 'subordinate_head_final': 0}
	valency_dictionary = {'intransitive': 0, 'transitive': 0, 'ditransitive': 0}

	verb_mood_dictionary = {}
	for feature in verb_mood_features:
		verb_mood_dictionary['verb_mood_' + feature] = 0

	verb_number_dictionary = {}
	for feature in verb_number_features:
		verb_number_dictionary['verb_number_' + feature] = 0

	verb_tense_dictionary = {}
	for feature in verb_tense_features:
		verb_tense_dictionary['verb_tense_' + feature] = 0

	verb_aspect_dictionary = {}
	for feature in verb_aspect_features:
		verb_aspect_dictionary['verb_aspect_' + feature] = 0

	verb_voice_dictionary = {}
	for feature in verb_voice_features:
		verb_voice_dictionary['verb_voice_' + feature] = 0

	verb_evident_dictionary = {}
	for feature in verb_evident_features:
		verb_evident_dictionary['verb_evident_' + feature] = 0

	verb_form_dictionary = {}
	for feature in verb_form_features:
		verb_form_dictionary['verb_form_' + feature] = 0

	verb_polarity_dictionary = {}
	for feature in verb_polarity_features:
		verb_polarity_dictionary['verb_polariy_' + feature] = 0

	verb_person_dictionary = {}
	for feature in verb_person_features:
		verb_person_dictionary['verb_person_' + feature] = 0

	verb_polite_dictionary = {}
	for feature in verb_polite_features:
		verb_polite_dictionary['verb_polite_' + feature] = 0

	verb_clusivity_dictionary = {}
	for feature in verb_clusivity_features:
		verb_clusivity_dictionary['verb_clusivity_' + feature] = 0

	aux_mood_dictionary = {}
	for feature in verb_mood_features:
		aux_mood_dictionary['aux_mood_' + feature] = 0

	aux_number_dictionary = {}
	for feature in verb_number_features:
		aux_number_dictionary['aux_number_' + feature] = 0

	aux_tense_dictionary = {}
	for feature in verb_tense_features:
		aux_tense_dictionary['aux_tense_' + feature] = 0

	aux_aspect_dictionary = {}
	for feature in verb_aspect_features:
		aux_aspect_dictionary['aux_aspect_' + feature] = 0

	aux_voice_dictionary = {}
	for feature in verb_voice_features:
		aux_voice_dictionary['aux_voice_' + feature] = 0

	aux_evident_dictionary = {}
	for feature in verb_evident_features:
		aux_evident_dictionary['aux_evident_' + feature] = 0

	aux_form_dictionary = {}
	for feature in verb_form_features:
		aux_form_dictionary['aux_form_' + feature] = 0

	aux_polarity_dictionary = {}
	for feature in verb_polarity_features:
		aux_polarity_dictionary['aux_polariy_' + feature] = 0

	aux_person_dictionary = {}
	for feature in verb_person_features:
		aux_person_dictionary['aux_person_' + feature] = 0

	aux_polite_dictionary = {}
	for feature in verb_polite_features:
		aux_polite_dictionary['aux_polite_' + feature] = 0

	aux_clusivity_dictionary = {}
	for feature in verb_clusivity_features:
		aux_clusivity_dictionary['aux_clusivity_' + feature] = 0

	non_projective_sent = 0
	non_projective_word = 0
	total_depth = 0

	subordinate_non_projective_sent = 0
	subordinate_non_projective_word = 0
	subordinate_total_depth = 0

	with io.open(file_handle, encoding = 'utf-8') as f:

		sent = conll_read_sentence(f)
		
		while sent is not None:

			G = nx.DiGraph()
			for tok in sent:
				G.add_edge(int(tok[6]), int(tok[0]))
			try:
				ns, nw, max_depth = analyze(G)
			except:
				print(file, sent)
			non_projective_sent += ns 
			non_projective_word += nw
			total_depth += max_depth

			num_sent += 1
			num_word += len(sent)

			for tok in sent:
				word_list.append(tok[1])
				word_len_list.append(len(tok[1]))
				lemma_list.append(tok[2])
				lemma_len_list.append(len(tok[2]))
				pos_list.append(tok[3])
				deprel_list.append(tok[7])

				if int(tok[6]) != 0:
					deplen_list.append(abs(int(tok[6]) - int(tok[0])))
					if int(tok[6]) > int(tok[0]):
						headedness_list.append('final')
					else:
						headedness_list.append('initial')

				if tok[3] in function_POS:
					function_word += 1
					function_word_list.append(tok[1])
					function_lemma_list.append(tok[1])

				if tok[3] == 'VERB':
					verb_word_list.append(tok[1])
					verb_lemma_list.append(tok[2])
					mood_feature, number_feature, person_feature, tense_feature, form_feature, aspect_feature, voice_feature, evident_feature, polarity_feature, polite_feature, clusivity_feature = verbal_inflection(tok[0], sent)
					if mood_feature != '':
						verb_mood_list.append(mood_feature)
					if number_feature != '':
						verb_number_list.append(number_feature)
					if person_feature != '':
						verb_person_list.append(person_feature)
					if tense_feature != '':
						verb_tense_list.append(tense_feature)
					if form_feature != '':
						verb_form_list.append(form_feature)
					if aspect_feature != '':
						verb_aspect_list.append(aspect_feature)
					if voice_feature != '':
						verb_voice_list.append(voice_feature)
					if evident_feature != '':
						verb_evident_list.append(evident_feature)
					if polarity_feature != '':
						verb_polarity_list.append(polarity_feature)
					if polite_feature != '':
						verb_polite_list.append(polite_feature)
					if clusivity_feature != '':
						verb_clusivity_list.append(clusivity_feature)

					if 'verb_mood_' + mood_feature in verb_mood_dictionary:
						verb_mood_dictionary['verb_mood_' + mood_feature] += 1
					if 'verb_number_' + number_feature in verb_number_dictionary:
						verb_number_dictionary['verb_number_' + number_feature] += 1
					if 'verb_person_' + person_feature in verb_person_dictionary:
						verb_person_dictionary['verb_person_' + person_feature] += 1
					if 'verb_tense_' + tense_feature in verb_tense_dictionary:
						verb_tense_dictionary['verb_tense_' + tense_feature] += 1
					if 'verb_form_' + form_feature in verb_form_dictionary:
						verb_form_dictionary['verb_form_' + form_feature] += 1
					if 'verb_aspect_' + aspect_feature in verb_aspect_dictionary:
						verb_aspect_dictionary['verb_aspect_' + aspect_feature] += 1
					if 'verb_voice_' + voice_feature in verb_voice_dictionary:
						verb_voice_dictionary['verb_voice_' + voice_feature] += 1
					if 'verb_evident_' + evident_feature in verb_evident_dictionary:
						verb_evident_dictionary['verb_evident_' + evident_feature] += 1
					if 'verb_polarity_' + polarity_feature in verb_polarity_dictionary:
						verb_polarity_dictionary['verb_polarity_' + polarity_feature] += 1
					if 'verb_polite_' + polite_feature in verb_polite_dictionary:
						verb_polite_dictionary['verb_polite_' + polite_feature] += 1
					if 'verb_clusivity_' + clusivity_feature in verb_clusivity_dictionary:
						verb_clusivity_dictionary['verb_clusivity_' + clusivity_feature] += 1

					order = word_order(tok[0], sent)
					if 'o' in order and 'io' in order:
						verb_valency_list.append('ditransitive')
						valency_dictionary['ditransitive'] += 1
					if 'o' in order and 'io' not in order:
						verb_valency_list.append('transitive')
						valency_dictionary['transitive'] += 1
					if 'o' not in order and 'io' in order:
						verb_valency_list.append('v_io')
					if 'o' not in order and 'io' not in order:
						verb_valency_list.append('intransitive')
						valency_dictionary['intransitive'] += 1

					try:
						if int(order.index('s')) < int(order.index('v')):
							word_order_dictionary['s_v'] += 1
					except:
						pass
					try:
						if int(order.index('s')) > int(order.index('v')):
							word_order_dictionary['v_s'] += 1
					except:
						pass 
					try:
						if int(order.index('o')) < int(order.index('v')):
							word_order_dictionary['o_v'] += 1
					except:
						pass
					try:
						if int(order.index('o')) > int(order.index('v')):
							word_order_dictionary['v_o'] += 1
					except:
						pass

					word_order_list.append('_'.join(w for w in order))

				if tok[3] == 'AUX':
					aux_word_list.append(tok[1])
					aux_lemma_list.append(tok[2])
					mood_feature, number_feature, person_feature, tense_feature, form_feature, aspect_feature, voice_feature, evident_feature, polarity_feature, polite_feature, clusivity_feature = verbal_inflection(tok[0], sent)
					if mood_feature != '':
						aux_mood_list.append(mood_feature)
					if number_feature != '':
						aux_number_list.append(number_feature)
					if person_feature != '':
						aux_person_list.append(person_feature)
					if tense_feature != '':
						aux_tense_list.append(tense_feature)
					if form_feature != '':
						aux_form_list.append(form_feature)
					if aspect_feature != '':
						aux_aspect_list.append(aspect_feature)
					if voice_feature != '':
						aux_voice_list.append(voice_feature)
					if evident_feature != '':
						aux_evident_list.append(evident_feature)
					if polarity_feature != '':
						aux_polarity_list.append(polarity_feature)
					if polite_feature != '':
						aux_polite_list.append(polite_feature)
					if clusivity_feature != '':
						aux_clusivity_list.append(clusivity_feature)

					if 'aux_mood_' + mood_feature in aux_mood_dictionary:
						aux_mood_dictionary['aux_mood_' + mood_feature] += 1
					if 'aux_number_' + number_feature in aux_number_dictionary:
						aux_number_dictionary['aux_number_' + number_feature] += 1
					if 'aux_person_' + person_feature in aux_person_dictionary:
						aux_person_dictionary['aux_person_' + person_feature] += 1
					if 'aux_tense_' + tense_feature in aux_tense_dictionary:
						aux_tense_dictionary['aux_tense_' + tense_feature] += 1
					if 'aux_form_' + form_feature in aux_form_dictionary:
						aux_form_dictionary['aux_form_' + form_feature] += 1
					if 'aux_aspect_' + aspect_feature in aux_aspect_dictionary:
						aux_aspect_dictionary['aux_aspect_' + aspect_feature] += 1
					if 'aux_voice_' + voice_feature in aux_voice_dictionary:
						aux_voice_dictionary['aux_voice_' + voice_feature] += 1
					if 'aux_evident_' + evident_feature in aux_evident_dictionary:
						aux_evident_dictionary['aux_evident_' + evident_feature] += 1
					if 'aux_polarity_' + polarity_feature in aux_polarity_dictionary:
						aux_polarity_dictionary['aux_polarity_' + polarity_feature] += 1
					if 'aux_polite_' + polite_feature in aux_polite_dictionary:
						aux_polite_dictionary['aux_polite_' + polite_feature] += 1
					if 'aux_clusivity_' + clusivity_feature in aux_clusivity_dictionary:
						aux_clusivity_dictionary['aux_clusivity_' + clusivity_feature] += 1

				if tok[7] in clauses:
					subordinate_deprel_list.append(tok[7])
					head = sent[int(tok[6]) - 1]
					if int(tok[6]) > int(tok[0]):
						subordinate_order_list.append(tok[7] + '_' + head[7])
						subordinate_order_dictionary['subordinate_head_final'] += 1
					else:
						subordinate_order_list.append(head[7] + '_' + tok[7])
						subordinate_order_dictionary['subordinate_head_initial'] += 1

					clause_subtree, clause_subtree_idx = subtree_generate(tok[0], sent)
					clause_len_list.append(len(clause_subtree))

					subordinate_G = nx.DiGraph()
					for z in clause_subtree:
						subordinate_G.add_edge(int(z[6]), int(z[0]))

					subordinate_ns, subordinate_nw, subordinate_max_depth = analyze(G)
					subordinate_non_projective_sent += subordinate_ns 
					subordinate_non_projective_word += subordinate_nw
					subordinate_total_depth += subordinate_max_depth

			sent = conll_read_sentence(f)

	num_word_type = len(set(word_list))
	function_word_type = len(set(function_word_list)) / num_word_type
	content_word = num_word - function_word
	content_word_type = 1 - function_word_type
	lexical_density = content_word / num_word

	function_word_H, function_word_std, function_word_range = distribution(function_word_list)
	function_lemma_H, function_lemma_std, function_lemma_range = distribution(function_lemma_list)

	num_lemma_type = len(set(lemma_list))
	function_lemma_type = len(set(function_lemma_list)) / num_lemma_type
	content_lemma_type = 1 - function_lemma_type

	num_pos_type = len(set(pos_list))
	pos_H, pos_std, pos_range = distribution(pos_list)

	ttr_word = num_word_type / num_word
	ttr_lemma = num_lemma_type / num_word

	ave_sent_len = num_word / num_sent
	ave_word_len = sum(word_len_list) / num_word
	ave_lemma_len = sum(lemma_len_list) / num_word

	verb_word_H, verb_word_std, verb_word_range = distribution(verb_word_list)
	verb_lemma_H, verb_lemma_std, verb_lemma_range = distribution(verb_lemma_list)
	verb_mood_H, verb_mood_std, verb_mood_range = distribution(verb_mood_list)
	verb_number_H, verb_number_std, verb_number_range = distribution(verb_number_list)
	verb_person_H, verb_person_std, verb_person_range = distribution(verb_person_list)
	verb_tense_H, verb_tense_std, verb_tense_range = distribution(verb_tense_list)
	verb_form_H, verb_form_std, verb_form_range = distribution(verb_form_list)
	verb_aspect_H, verb_aspect_std, verb_aspect_range = distribution(verb_aspect_list)
	verb_voice_H, verb_voice_std, verb_voice_range = distribution(verb_voice_list)
	verb_evident_H, verb_evident_std, verb_evident_range = distribution(verb_evident_list)
	verb_polarity_H, verb_polarity_std, verb_polarity_range = distribution(verb_polarity_list)
	verb_polite_H, verb_polite_std, verb_polite_range = distribution(verb_polite_list)
	verb_clusivity_H, verb_clusivity_std, verb_clusivity_range = distribution(verb_clusivity_list)

	verb_valency_H, verb_valency_std, verb_valency_range = distribution(verb_valency_list)

	aux_word_H, aux_word_std, aux_word_range = distribution(aux_word_list)
	aux_lemma_H, aux_lemma_std, aux_lemma_range = distribution(aux_lemma_list)
	aux_mood_H, aux_mood_std, aux_mood_range = distribution(aux_mood_list)
	aux_number_H, aux_number_std, aux_number_range = distribution(aux_number_list)
	aux_person_H, aux_person_std, aux_person_range = distribution(aux_person_list)
	aux_tense_H, aux_tense_std, aux_tense_range = distribution(aux_tense_list)
	aux_form_H, aux_form_std, aux_form_range = distribution(aux_form_list)
	aux_aspect_H, aux_aspect_std, aux_aspect_range = distribution(aux_aspect_list)
	aux_voice_H, aux_voice_std, aux_voice_range = distribution(aux_voice_list)
	aux_evident_H, aux_evident_std, aux_evident_range = distribution(aux_evident_list)
	aux_polarity_H, aux_polarity_std, aux_polarity_range = distribution(aux_polarity_list)
	aux_polite_H, aux_polite_std, aux_polite_range = distribution(aux_polite_list)
	aux_clusivity_H, aux_clusivity_std, aux_clusivity_range = distribution(aux_clusivity_list)

	deprel_H , deprel_std, deprel_range = distribution(deprel_list)

	subordinate_deprel_H , subordinate_deprel_std, subordinate_deprel_range = distribution(subordinate_deprel_list)
	subordinate_order_H, subordinate_order_std, subordinate_order_range = distribution(subordinate_order_list)

	head_finality = headedness_list.count('final') / len(headedness_list)

	verb_valency_H, verb_valency_std, verb_valency_range = distribution(verb_valency_list)
	word_order_H, word_order_std, word_order_range = distribution(word_order_list)

	ave_dep_len = sum(deplen_list) / len(deplen_list)
	ave_clause_len = 0
	try:
		ave_clause_len = sum(clause_len_list) / len(clause_len_list)
	except:
		ave_clause_len = 0

	non_projective_sent_ratio = non_projective_sent / num_sent
	non_projective_word_ratio = non_projective_word / num_word
	ave_tree_depth = total_depth / num_sent

	subordinate_non_projective_sent_ratio = 0
	try:
		subordinate_non_projective_sent_ratio = subordinate_non_projective_sent / len(clause_len_list)
	except:
		subordinate_non_projective_sent_ratio = 0

	subordinate_non_projective_word_ratio = 0
	try:
		subordinate_non_projective_word_ratio = subordinate_non_projective_word / sum(clause_len_list)
	except:
		subordinate_non_projective_word_ratio = 0

	subordinate_ave_tree_depth = 0
	try:
		subordinate_ave_tree_depth = subordinate_total_depth / len(clause_len_list)
	except:
		subordinate_ave_tree_depth = 0

	verb_ratio = len(verb_word_list) / num_sent

	verb_features = [verb_mood_dictionary, verb_number_dictionary, verb_person_dictionary, verb_tense_dictionary, verb_form_dictionary, verb_aspect_dictionary, verb_voice_dictionary, verb_evident_dictionary, verb_polarity_dictionary, verb_polite_dictionary, verb_clusivity_dictionary]
	aux_features = [aux_mood_dictionary, aux_number_dictionary, aux_person_dictionary, aux_tense_dictionary, aux_form_dictionary, aux_aspect_dictionary, aux_voice_dictionary, aux_evident_dictionary, aux_polarity_dictionary, aux_polite_dictionary, aux_clusivity_dictionary]

	return [num_sent, ave_sent_len, num_word, num_word_type, ttr_word, ave_word_len, function_word_type, function_word_H, function_word_std, function_word_range, lexical_density,
	num_lemma_type, ttr_lemma, ave_lemma_len, function_lemma_type, function_lemma_H, function_lemma_std, function_lemma_range, num_pos_type, pos_H, pos_std, pos_range, 
	verb_word_H, verb_word_std, verb_word_range, verb_lemma_H, verb_lemma_std, verb_lemma_range, verb_mood_H, verb_mood_std, verb_mood_range, verb_number_H, verb_number_std, verb_number_range, verb_person_H, verb_person_std, verb_person_range,
	verb_tense_H, verb_tense_std, verb_tense_range, verb_form_H, verb_form_std, verb_form_range, verb_valency_H, verb_valency_std, verb_valency_range, verb_aspect_H, verb_aspect_std, verb_aspect_range, verb_voice_H, verb_voice_std, verb_voice_range,
	verb_evident_H, verb_evident_std, verb_evident_range, verb_polarity_H, verb_polarity_std, verb_polarity_range, verb_polite_H, verb_polite_std, verb_polite_range, verb_clusivity_H, verb_clusivity_std, verb_clusivity_range,
	aux_word_H, aux_word_std, aux_word_range, aux_lemma_H, aux_lemma_std, aux_lemma_range, aux_mood_H, aux_mood_std, aux_mood_range, aux_number_H, aux_number_std, aux_number_range, aux_person_H, aux_person_std, aux_person_range,
	aux_tense_H, aux_tense_std, aux_tense_range, aux_form_H, aux_form_std, aux_form_range, aux_aspect_H, aux_aspect_std, aux_aspect_range, aux_voice_H, aux_voice_std, aux_voice_range,
	aux_evident_H, aux_evident_std, aux_evident_range, aux_polarity_H, aux_polarity_std, aux_polarity_range, aux_polite_H, aux_polite_std, aux_polite_range, aux_clusivity_H, aux_clusivity_std, aux_clusivity_range,
	deprel_H , deprel_std, deprel_range, subordinate_deprel_H, subordinate_deprel_std, subordinate_deprel_range, subordinate_order_H, subordinate_order_std, subordinate_order_range,
	head_finality, verb_valency_H, verb_valency_std, verb_valency_range, word_order_H, word_order_std, word_order_range, ave_dep_len, ave_clause_len,
	non_projective_sent_ratio, non_projective_word_ratio, ave_tree_depth, subordinate_non_projective_sent, subordinate_non_projective_word_ratio, subordinate_ave_tree_depth,
	verb_ratio], word_order_dictionary, subordinate_order_dictionary, verb_features, aux_features
  

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to conllu')
	parser.add_argument('--output', type = str, help = 'output .txt file of features')

	args = parser.parse_args()

	outfile = io.open('features.txt', 'w', encoding = 'utf-8')
	header = ['num_sent', 'ave_sent_len', 'num_word', 'num_word_type', 'ttr_word', 'ave_word_len', 'function_word_type', 'function_word_H', 'function_word_std', 'function_word_range', 'lexical_density',
			'num_lemma_type', 'ttr_lemma', 'ave_lemma_len', 'function_lemma_type', 'function_lemma_H', 'function_lemma_std', 'function_lemma_range', 'num_pos_type', 'pos_H', 'pos_std', 'pos_range', 
			'verb_word_H', 'verb_word_std', 'verb_word_range', 'verb_lemma_H', 'verb_lemma_std', 'verb_lemma_range', 'verb_mood_H', 'verb_mood_std', 'verb_mood_range', 'verb_number_H', 'verb_number_std', 'verb_number_range', 'verb_person_H', 'verb_person_std', 'verb_person_range',
			'verb_tense_H', 'verb_tense_std', 'verb_tense_range', 'verb_form_H', 'verb_form_std', 'verb_form_range', 'verb_valency_H', 'verb_valency_std', 'verb_valency_range', 'verb_aspect_H', 'verb_aspect_std', 'verb_aspect_range', 'verb_voice_H', 'verb_voice_std', 'verb_voice_range',
			'verb_evident_H', 'verb_evident_std', 'verb_evident_range', 'verb_polarity_H', 'verb_polarity_std', 'verb_polarity_range', 'verb_polite_H', 'verb_polite_std', 'verb_polite_range', 'verb_clusivity_H', 'verb_clusivity_std', 'verb_clusivity_range',
			'aux_word_H', 'aux_word_std', 'aux_word_range', 'aux_lemma_H', 'aux_lemma_std', 'aux_lemma_range', 'aux_mood_H', 'aux_mood_std', 'aux_mood_range', 'aux_number_H', 'aux_number_std', 'aux_number_range', 'aux_person_H', 'aux_person_std', 'aux_person_range',
			'aux_tense_H', 'aux_tense_std', 'aux_tense_range', 'aux_form_H', 'aux_form_std', 'aux_form_range', 'aux_aspect_H', 'aux_aspect_std', 'aux_aspect_range', 'aux_voice_H', 'aux_voice_std', 'aux_voice_range',
			'aux_evident_H', 'aux_evident_std', 'aux_evident_range', 'aux_polarity_H', 'aux_polarity_std', 'aux_polarity_range', 'aux_polite_H', 'aux_polite_std', 'aux_polite_range', 'aux_clusivity_H', 'aux_clusivity_std', 'aux_clusivity_range',
			'deprel_H' , 'deprel_std', 'deprel_range', 'subordinate_deprel_H', 'subordinate_deprel_std', 'subordinate_deprel_range', 'subordinate_order_H', 'subordinate_order_std', 'subordinate_order_range',
			'head_finality', 'verb_valency_H', 'verb_valency_std', 'verb_valency_range', 'word_order_H', 'word_order_std', 'word_order_range', 'ave_dep_len', 'ave_clause_len',
			'non_projective_sent_ratio', 'non_projective_word_ratio', 'ave_tree_depth', 'subordinate_non_projective_sent', 'subordinate_non_projective_word_ratio', 'subordinate_ave_tree_depth', 'verb_raio']
			
	for file in os.listdir(args.input + 'Arabe/'):
		if file.endswith('.conllu') and file == '28.conllu':
			all_info, word_order_dictionary, subordinate_order_dictionary, verb_features, aux_features = full_analyze(args.input + 'Arabe/' + file)

	for k, v in word_order_dictionary.items():
		header.append(k)

	for k, v in subordinate_order_dictionary.items():
		header.append(k)

	for feature_dictionary in verb_features:
		for k, v in feature_dictionary.items():
			header.append(k)

	for feature_dictionary in aux_features:
		for k, v in feature_dictionary.items():
			header.append(k)

	header.append('Lang')

	outfile.write('\t'.join(w for w in header) + '\n')

	for folder in os.listdir(args.input):
		print(folder)
		if os.path.isdir(args.input + folder + '/') is True:
			for file in os.listdir(args.input + folder + '/'):
				lang = folder

				if file.endswith('.conllu'): # and folder in ['ar']: # and folder not in ['ja', 'it', 'zh', 'te']:# and file == '6514.conllu':
		#	num_sent, ave_sent_len, num_word, num_word_type, ttr_word, ave_word_len, function_word_type, function_word_H, function_word_std, function_word_range, lexical_density,
		#	num_lemma_type, ttr_lemma, ave_lemma_len, function_lemma_type, function_lemma_H, function_lemma_std, function_lemma_range, num_pos_type, pos_H, pos_std, pos_range, 
		#	verb_word_H, verb_word_std, verb_word_range, verb_lemma_H, verb_lemma_std, verb_lemma_range, verb_mood_H, verb_mood_std, verb_mood_range, verb_number_H, verb_number_std, verb_number_range, verb_person_H, verb_person_std, verb_person_range,
		#	verb_tense_H, verb_tense_std, verb_tense_range, verb_form_H, verb_form_std, verb_form_range, verb_valency_H, verb_valency_std, verb_valency_range, verb_aspect_H, verb_aspect_std, verb_aspect_range, verb_voice_H, verb_voice_std, verb_voice_range,
		#	verb_evident_H, verb_evident_std, verb_evident_range, verb_polarity_H, verb_polarity_std, verb_polarity_range, verb_polite_H, verb_polite_std, verb_polite_range, verb_clusivity_H, verb_clusivity_std, verb_clusivity_range,
		#	aux_word_H, aux_word_std, aux_word_range, aux_lemma_H, aux_lemma_std, aux_lemma_range, aux_mood_H, aux_mood_std, aux_mood_range, aux_number_H, aux_number_std, aux_number_range, aux_person_H, aux_person_std, aux_person_range,
		#	aux_tense_H, aux_tense_std, aux_tense_range, aux_form_H, aux_form_std, aux_form_range, aux_valency_H, aux_valency_std, aux_valency_range, aux_aspect_H, aux_aspect_std, aux_aspect_range, aux_voice_H, aux_voice_std, aux_voice_range,
		#	aux_evident_H, aux_evident_std, aux_evident_range, aux_polarity_H, aux_polarity_std, aux_polarity_range, aux_polite_H, aux_polite_std, aux_polite_range, aux_clusivity_H, aux_clusivity_std, aux_clusivity_range,
		#	deprel_H , deprel_std, deprel_range, subordinate_deprel_H, subordinate_deprel_std, subordinate_deprel_range, subordinate_order_H, subordinate_order_std, subordinate_order_range,
		#	head_finality, verb_valency_H, verb_valency_std, verb_valency_range, word_order_H, word_order_std, word_order_range, ave_dep_len, ave_clause_len,
		#	non_projective_sent_ratio, non_projective_word_ratio, ave_tree_depth, subordinate_non_projective_sent, subordinate_non_projective_word_ratio, subordinate_ave_tree_depth,
		#	verb_raio, word_order_dictionary, subordinate_order_dictionary = analyze(args.input + file)
					try:
						all_info, word_order_dictionary, subordinate_order_dictionary, verb_features, aux_features = full_analyze(args.input + folder + '/' + file)
						word_order_dictionary = dictionary_ratio(word_order_dictionary)
						for k, v in word_order_dictionary.items():
							all_info.append(v)

						subordinate_order_dictionary = dictionary_ratio(subordinate_order_dictionary)
						for k, v in subordinate_order_dictionary.items():
							all_info.append(v)

						for feature_dictionary in verb_features:
							feature_dictionary = dictionary_ratio(feature_dictionary)
							for k, v in feature_dictionary.items():
								all_info.append(v)

						for feature_dictionary in aux_features:
							feature_dictionary = dictionary_ratio(feature_dictionary)
							for k, v in feature_dictionary.items():
								all_info.append(v)

						all_info.append(lang)

						outfile.write('\t'.join(str(w) for w in all_info) + '\n')

					except:
						print(file)



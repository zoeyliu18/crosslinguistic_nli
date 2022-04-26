import io, os

if 'UD_Italian-Valico' not in os.listdir('resources/'):
	os.system('git clone https://github.com/UniversalDependencies/UD_Italian-Valico')
	os.system('mv UD_Italian-Valico resources/')

if not os.path.exists('data/UD_Italian-Valico'):
	os.system('mkdir data/UD_Italian-Valico')

def get_info(file):	

	info_list = []
	en_text_list = []
	fr_text_list = []
	de_text_list = []
	es_text_list = []

	with io.open(file) as f:
		for line in f:
			if '# sent_id = ' in line:
				line = line.strip().split()
				info = line[-1].split('-')[ : -1]
				text_id = info[0]
				info = '-'.join(w for w in info)
				info = info.split('_')
				lg_code = info[-1]
				info_list.append([text_id, lg_code])
				if lg_code == 'en':
					en_text_list.append(int(text_id))
				if lg_code == 'fr':
					fr_text_list.append(int(text_id))
				if lg_code == 'de':
					de_text_list.append(int(text_id))
				if lg_code == 'es':
					es_text_list.append(int(text_id))

	en_text_list.sort()
	fr_text_list.sort()
	de_text_list.sort()
	es_text_list.sort()

	return info_list, en_text_list, fr_text_list, de_text_list, es_text_list


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


file = 'resources/UD_Italian-Valico/it_valico-ud-test.conllu'
info_list, en_text_list, fr_text_list, de_text_list, es_text_list = get_info(file)

lg_directory = {'en': 'English', 'fr': 'French', 'de': 'German', 'es': 'Spanish'}
text_id_directory = {'en': en_text_list, 'fr': fr_text_list, 'de': de_text_list, 'es': es_text_list}

if not os.path.exists('data/UD_Italian-Valico/English'):
	os.system('mkdir data/UD_Italian-Valico/English')

if not os.path.exists('data/UD_Italian-Valico/French'):
	os.system('mkdir data/UD_Italian-Valico/French')

if not os.path.exists('data/UD_Italian-Valico/German'):
	os.system('mkdir data/UD_Italian-Valico/German')

if not os.path.exists('data/UD_Italian-Valico/Spanish'):
	os.system('mkdir data/UD_Italian-Valico/Spanish')

data = []

with io.open(file) as f:
	sent = conll_read_sentence(f)
	while sent is not None:
		data.append(' '.join(tok[1] for tok in sent))
		sent = conll_read_sentence(f)

assert len(info_list) == len(data)

print(data)

for k, v in lg_directory.items():
	print(k)
	lg = lg_directory[k]
	for text_id in text_id_directory[k]:
		with io.open('data/UD_Italian-Valico/' + lg + '/' + str(text_id) + '.txt', 'w') as f:
			for i in range(len(info_list)):
				text_info = info_list[i]
				lg_code = text_info[-1]
				if lg_code == k and text_info[0] == str(text_id):
					sent = data[i]
					f.write(sent + '\n')



			
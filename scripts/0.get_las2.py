import io, os
from bs4 import BeautifulSoup

if not os.path.exists('data/LAS2'):
	os.system('mkdir data/LAS2')

lg_directory = {'cs': 'Czech', 'de': 'German', 'en': 'English', 'et': 'Estonian', 'hu': 'Hungarian', 'is': 'Icelandic', 'ja': 'Japanese', 'kv': 'Komi', 'lt': 'Lithuanian', 'pl': 'Polish', 'ru': 'Russian', 'sv': 'Swedish'}

for directory in os.listdir('resources/LAS2_language-bank-version/'):
	if directory in ['L2_essay', 'L2_exam']:
		for file in os.listdir('resources/LAS2_language-bank-version/' + directory):
			if file.endswith('xml'):
				lg_code = ''
				
				data = []
				with io.open('resources/LAS2_language-bank-version/' + directory + '/' + file) as f:
					for line in f:
						line = line.strip()
						if line.startswith('<teksti'):
							toks = line.split()
							for tok in toks:
								if tok.startswith('l1='):
									while '"' in tok:
										tok = tok.replace('"', '')
										lg_code = tok.split('=')[1]

						if line.startswith('<w lemma='):
							toks = line.split('>')[1].split('<')[0]
							data.append(toks)

				if lg_code in lg_directory:
					lg = lg_directory[lg_code]

					if not os.path.exists('data/LAS2/' + lg):
						os.system('mkdir data/LAS2/' + lg)

					file_name = file.split('.')[0]

					with io.open('data/LAS2/' + lg + '/' + file_name + '.txt', 'w') as f:
						f.write(' '.join(w for w in data))

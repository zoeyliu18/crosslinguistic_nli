import io, os
from bs4 import BeautifulSoup

if not os.path.exists('data/CLC'):
	os.system('mkdir data/CLC')

idx = 1

for directory in os.listdir('resources/fce-released-dataset/dataset/'):
	for file in os.listdir('resources/fce-released-dataset/dataset/' + directory):
		if file.endswith('xml'):
			f = io.open('resources/fce-released-dataset/dataset/' + directory + '/' + file).read()
			soup = BeautifulSoup(f, 'xml')
			lg = soup.find_all('language')[0].get_text()
			if not os.path.exists('data/CLC/' + lg):
				os.system('mkdir data/CLC/' + lg)

			answer1 = soup.find_all('answer1')
			answer1_data = []
			for tok in answer1:
				tok = tok.text.split('\n')
				for s in tok:
					if s != '':
						answer1_data.append(s)
			answer1_data = answer1_data[2 : ]

			with io.open('data/CLC/' + lg + '/' + str(idx) + '.txt', 'w') as f:
				for tok in answer1_data:
					f.write(tok + '\n')

			idx += 1

			answer2 = soup.find_all('answer1')
			answer2_data = []
			for tok in answer2:
				tok = tok.text.split('\n')
				for s in tok:
					if s != '':
						answer2_data.append(s)
			answer2_data = answer2_data[2 : ]

			with io.open('data/CLC/' + lg + '/' + str(idx) + '.txt', 'w') as f:
				for tok in answer1_data:
					f.write(tok + '\n')

			idx += 1

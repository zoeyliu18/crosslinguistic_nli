import io, os
from bs4 import BeautifulSoup

if not os.path.exists('data/ASK'):
	os.system('mkdir data/ASK')

lg_directory = {'albansk': 'Albanian', 'engelsk': 'English', 'nederlandsk': 'Dutch', 'polsk': 'Polish', 'russik': 'Russian', 'serbokroatisk': 'Bosnian-Croatian-Serbian', 'somali': 'Somali', 'spansk': 'Spanish', 'tysk': 'German', 'vietnamesisk': 'Vietnamese'}

for file in os.listdir('resources/ASK/'):
	if file.endswith('xml'):
		lg_code = ''
		with io.open('resources/ASK/' + file) as f:
			for line in f:
				if 'n="language">' in line:
					lg_code = line.strip().split('>')[1].split('<')[0]

		if lg_code in lg_directory:
			lg = lg_directory[lg_code]

			if not os.path.exists('data/ASK/' + lg):
				os.system('mkdir data/ASK/' + lg)

			f = io.open('resources/ASK/' + file).read()
			soup = BeautifulSoup(f, 'xml')
			words = soup.find_all('word')
			data = []

			for word in words:
				word = word.text 
				data.append(word)

			if data[0] == 'Oppgave':
				data = data[4 : ]

			file_name = file.split('.')[0]

			with io.open('data/ASK/' + lg + '/' + file_name + '.txt', 'w') as f:
				f.write(' '.join(w for w in data))

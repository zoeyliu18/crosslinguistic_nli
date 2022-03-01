import io, os, argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to resources/')
	parser.add_argument('--output', type = str, help = 'path to processed/')
	parser.add_argument('--lg', type = str, help = 'en, es, hr')

	args = parser.parse_args()

	for directory in os.listdir(args.input):
		if directory in ['CEDEL']: #['TOEFL', 'PELIC', 'WriCLE_formal', 'WriCLE_informal', 'CAES', 'COWS']:
			if not os.path.exists(args.output + directory):
				os.system('mkdir ' + args.output + directory)
			
			for language in os.listdir(args.input + directory):
				if not os.path.exists(args.output + directory + '/' + language):
					os.system('mkdir ' + args.output + directory + '/' + language)

				for file in os.listdir(args.input + directory + '/' + language):
					data = []
					with io.open(args.input + directory + '/' + language + '/' + file) as f:
						for line in f:
							line = line.strip()
							for i in range(len(line)):
								c = line[i]
								if c not in ['¡', '?', '?', '.', '!']:
									data.append(c)
								else:
									data.append(c)
									data.append('-SENT-')

					sentences = ''.join(c for c in data)
					sentences = sentences.split('-SENT-')
					new_sentences = []
					for sent in sentences:
						if len(sent) != 0:
							new_sentences.append(sent)

					with io.open(args.output + directory + '/' + language + '/' + file, 'w') as f:
						for sent in new_sentences:
							if sent[0] == ' ':
								sent = sent[1 : ]
							f.write(sent + '\n')


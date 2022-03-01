import io, os, argparse

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

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to parsed/')
	parser.add_argument('--output', type = str, help = 'path to results/')

	args = parser.parse_args()

	for corpus in os.listdir(args.input):
		print(corpus)
		for folder in os.listdir(args.input + corpus + '/'):
			print(folder)
			if os.path.isdir(args.input + corpus + '/' + folder + '/') is True:
				for file in os.listdir(args.input + corpus + '/' + folder + '/'):
					lang = folder

					if file.endswith('.conllu'): 
						with io.open(args.input + corpus + '/' + folder + '/' + file) as f:
							sent = conll_read_sentence(f)
							while sent is not None:
								roots = 0
								for tok in sent:
									if tok[7] == 'root':
										roots += 1

								if roots > 1:
									print(file)
									for tok in sent:
										print(tok)
									print('\n')

								sent = conll_read_sentence(f)

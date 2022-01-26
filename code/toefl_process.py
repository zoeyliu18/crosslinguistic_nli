### Generate descriptive information for the TOEFL data sets ###
### Prepare TOEFL data sets for BERT classification ###

import io, os, string, argparse, random

def read_file(file):

	file_data = []
	sent_count = 0
	word_count = 0

	with io.open(file, encoding = 'utf-8') as f:
		for line in f:
			if line != '':
				line = line.strip()
				sent_count += 1
				toks = line.split()
				word_count += len(toks)
				file_data.append(line)

	return '\t'.join(sent for sent in file_data), sent_count, word_count


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to TOEFL data')
	parser.add_argument('--output', type = str, help = 'output training/test file')

	args = parser.parse_args()

	train_data = []
	test_data = []

	lg_info = {}

	HELDOUT_RATE = 0.2

	for lg in os.listdir(args.input):

		lg_data = []
		lg_sent_count = []
		lg_word_count = []

		count = 0

		if lg != '.DS_Store':

			for file in os.listdir(args.input + lg + '/'):
				if file.endswith('.txt'):
					count += 1
					file_data, sent_count, word_count = read_file(args.input + lg + '/' + file)
					lg_data.append(' ## '.join(w for w in [file_data, lg]))
					lg_sent_count.append(sent_count)
					lg_word_count.append(word_count)

			lg_info[lg] = [count, sum(lg_word_count), sum(lg_sent_count)]
	
			random.shuffle(lg_data)

			lg_train_num = int(count * (1 - HELDOUT_RATE))

			lg_train_data = lg_data[ : lg_train_num]
			lg_test_data = lg_data[lg_train_num : ]

			train_data += lg_train_data
			test_data += lg_test_data

	with io.open(args.output + 'TOEFL_descriptive.txt', 'w', encoding = 'utf-8') as f:
		header = ['Language', 'Avg. word count', 'Total word count', 'Avg. sent count', 'Total sent count', 'N of essays']
		f.write('\t'.join(w for w in header) + '\n')
	
		for k, v in lg_info.items():
			lg = k
			avg_word_count = round(v[1] / v[0], 2)
			avg_sent_count = round(v[2] / v[0], 2)
		
			f.write('\t'.join(str(w) for w in [lg, avg_word_count, v[1], avg_sent_count, v[2], v[0]]) + '\n')
'''			
	random.shuffle(train_data)
	random.shuffle(test_data)

	with io.open(args.output + 'TOEFL_bert_train.txt', 'w', encoding = 'utf-8') as f:
		for tok in train_data:
			f.write(tok + '\n')

	with io.open(args.output + 'TOEFL_bert_test.txt', 'w', encoding = 'utf-8') as f:
		for tok in test_data:
			f.write(tok + '\n')

'''	


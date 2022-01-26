import io, os, argparse, random, statistics, math
import pandas as pd

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input path to conllu')
#	parser.add_argument('--output', type = str, help = 'output .txt file of features')

	args = parser.parse_args()

	all_data = pd.DataFrame()

	for file in os.listdir(args.input):
		if file.endswith('csv'):
			lang = file.split('.')[0]
			lang_data = pd.read_csv(args.input + file, sep = '\t', encoding = 'utf-8')
			lang_data = pd.DataFrame(lang_data)
			num = len(lang_data)
			lang_column = []
			for i in range(num):
				lang_column.append(lang)

			lang_data['Lang'] = lang_column

			all_data = pd.concat([all_data, lang_data], axis = 0)

	header = list(all_data.columns)
	print(len(header))
	all_data.to_csv('toefl_profile_features.txt', index = False)

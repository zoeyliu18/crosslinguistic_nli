import io, os
from bs4 import BeautifulSoup

if not os.path.exists('data/TOCFL'):
	os.system('mkdir data/TOCFL')

data = []
l1_list = []
for file in os.listdir('resources/TOCFL/'):
	if file.endswith('sgml') and 'Sample' not in file:
		file_name = file.split('.')[0]
	#	os.system('cat resources/TOCFL/' + file + ' > resources/TOCFL/' + file_name + '.txt')
		with io.open('resources/TOCFL/' + file_name + '.txt') as f:
			for line in f:
				data.append(line.strip())
				if line.startswith('<L1>'):
					l1_list.append(line.strip()[4 : -5])


essay_idx_list = []

for i in range(len(data)):
	tok = data[i]
	if tok.startswith('<ESSAY id='):
		essay_idx_list.append(i)


essay_list = []

for i in range(len(essay_idx_list)):
	essay = []

	sent_start_idx_list = []
	sent_end_idx_list = []
	try:
		essay_idx = essay_idx_list[i]
		for idx in range(essay_idx, essay_idx_list[i + 1]):
			line = data[idx]
			if line.startswith('<P>'):
				sent_start_idx_list.append(idx)
			if line.startswith('</P>'):
				sent_end_idx_list.append(idx)

	except:
		essay_idx = essay_idx_list[i]
		for idx in range(essay_idx, len(data)):
			line = data[idx]
			if line.startswith('<P>'):
				sent_start_idx_list.append(idx)
			if line.startswith('</P>'):
				sent_end_idx_list.append(idx)

	
	for z in sent_start_idx_list:
		text = data[z + 1]
		essay.append(text)

	essay_list.append(essay)

idx = 1
filter_l1 = []
for i in range(len(l1_list)):
	l1 = l1_list[i]
	essay = essay_list[i]
	if '/' not in l1 and l1 != 'null':
		filter_l1.append(l1)
		with io.open('data/TOCFL/' + l1 + '_' + str(idx) + '.txt', 'w') as f:
			for sent in essay:
				f.write(sent + '\n')

		idx += 1

for l1 in set(filter_l1):
	print(l1)

		
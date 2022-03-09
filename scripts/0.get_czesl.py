import io, os

lg_directory = {'ar': 'Arabic', 'az': 'Azerbaijani', 'ba': 'Bashkir', 'be': 'Belarusian', 'bg': 'Bulgarian', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'ka': 'Georgian', 'kg': 'Kongo', 'kk': 'Kazakh', 'ko': 'Korean', 'ky': 'Kirghiz', 'lv': 'Latvian', 'mk': 'Macedonian', 'mn': 'Mongolian', 'mo': 'Moldavian', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanina', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sq': 'Albanian', 'sr': 'Serbian', 'sv': 'Swedish', 'tg': 'tajik', 'th': 'Thai', 'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukranian', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'xal': 'Kalmyk', 'zh': 'Chinese'}

if not os.path.exists('data/Czesl'):
	os.system('mkdir data/Czesl')

file = 'resources/2014-czesl-sgt-en-all-v2'

data = []

with io.open(file) as f:
	for line in f:
		line = line.strip()
		data.append(line)

div_idx_list = []
end_div_idx_list = []

for i in range(len(data)):
	tok = data[i]
	if tok.startswith('<div t_id'):
		div_idx_list.append(i)
	if tok.startswith('</div>'):
		end_div_idx_list.append(i)

assert len(div_idx_list) == len(end_div_idx_list)

idx = 1

for i in range(len(div_idx_list)):
	info = data[div_idx_list[i]]
	info = info.split()
	bilingual = 'yes'
	lg_code = ''
	for tok in info:
		if tok.startswith('s_L1='):
			lg_code = tok.split('=')[1]
			while '"' in lg_code:
				lg_code = lg_code.replace('"', '')

		if tok.startswith('s_bilingual="no'):
			bilingual = 'no'

	if lg_code != '' and lg_code not in ['la', 'ms', 'sh'] and bilingual == 'no':
		lg = lg_directory[lg_code]
		if not os.path.exists('data/Czesl/' + lg):
			os.system('mkdir data/Czesl/' + lg)

		document = []

		start = div_idx_list[i]
		end = end_div_idx_list[i]
		sent_idx_list = []
		end_sent_idx_list = []

		for z in range(start, end + 1):
			tok = data[z]
			if tok.startswith('<s '):
				sent_idx_list.append(z)
			if tok.startswith('</s>'):
				end_sent_idx_list.append(z)

		assert len(sent_idx_list) == len(end_sent_idx_list)

		for w in range(len(sent_idx_list)):
			sent_start = sent_idx_list[w]
			sent_end = end_sent_idx_list[w]

			sent = []

			for tok in data[sent_start: sent_end + 1]:
				if tok.startswith('<word '):
					tok = tok.split()
					for w in tok:
						if w.startswith('word1'):
							w = w.split('=')[1]
							while '"' in w:
								w = w.replace('"', '')
							if w != 'XXX':
								sent.append(w)

			document.append(' '.join(w for w in sent))

		with io.open('data/Czesl/' + lg + '/' + str(idx) + '.txt', 'w') as f:
			for sent in document:
				f.write(sent + '\n')

		idx += 1




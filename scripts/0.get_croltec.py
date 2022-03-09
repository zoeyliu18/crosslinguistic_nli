import requests, os, argparse
from lxml import html

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type = str, help = 'wget url or generate text from url')

args = parser.parse_args()

if args.mode == 'url':
	URL = "http://teitok.clul.ul.pt/croltec/index.php?action=files"
	top_level = requests.get(URL)
	top_level_webpage = html.fromstring(top_level.content)
	top_level_webpage = top_level_webpage.xpath('//a/@href')

	for webpage in top_level_webpage:
		if "folder=xmlfiles" in webpage:
			url = "http://teitok.clul.ul.pt/croltec/" + webpage
			second_level = requests.get(url)
			second_level_webpage = html.fromstring(second_level.content)
			second_level_webpage = second_level_webpage.xpath('//a/@href')

			for second_webpage in second_level_webpage:
			#	if 'Final' in second_webpage:
			#		final_url = "http://teitok.clul.ul.pt/croltec/" + second_webpage
			#		final_level = requests.get(final_url)
			#		final_level_webpage = html.fromstring(final_level.content)
			#		final_level_webpage = final_level_webpage.xpath('//a/@href')
			#		for final_webpage in final_level_webpage:
			#			if 'Final/' in final_webpage:
			#				final_sub_url = "http://teitok.clul.ul.pt/croltec/" + final_webpage
			#				print("wget " + "'" + final_sub_url + "'")

			#	else:
				if 'Final' not in second_webpage:
					if 'xml' in second_webpage:
						second_url = "http://teitok.clul.ul.pt/croltec/" + second_webpage
						print("wget " + "'" + second_url + "'")

	

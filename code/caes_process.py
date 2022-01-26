### This scripts process CAES data sets to CoNLL formats with POS tags and dependency relations ###

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pylab as pl

import nltk, re, sys, io, os, pickle, operator, argparse

exam_list = [] # a list of all samples in the directory
langlist = ""
tagslist = ""
lengua = []  ### (mother) tongue
edad = [] ### age
nivel = [] ### level
meses_aprendiendo = [] ### months_learning


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'input to CAES data')
	parser.add_argument('--output', type = str, help = 'output .conllu file')

	args = parser.parse_args()
	idx = 0
	for file in os.listdir(args.input):
		if file.endswith('.xml'):
			
			data = []

			tree = ET.parse(args.input + file)
			root = tree.getroot()

			for cabecera in root.findall('cabecera'):
				lengua_materna = cabecera.find("lengua_materna").text
				lengua.append((lengua_materna))
				edad.append(cabecera.find("edad").text)
				meses_aprendiendo.append (cabecera.find("meses_aprendiendo_español").text)
				nivel.append(cabecera.find("nivel").text)

			langlist += (str(lengua_materna.encode('utf-8'))+"\n")
			
			if lengua_materna.startswith('Chino'):
				print(lengua_materna)
				for text in root.iter('texto'):
					data.append(text.text)

			if data != []:
				with io.open(args.output + str(idx) + '.txt', 'w', encoding = 'utf-8') as f:
					for tok in data:
						f.write(tok + '\n')

				idx += 1


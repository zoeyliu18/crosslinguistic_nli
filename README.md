# crosslinguistic_nli: Data-driven Crosslinguistic Morphosyntactic Transfer in Second Language Learning

## Installation
  - [Stanza](https://stanfordnlp.github.io/stanza/)
  - [Diaparser](https://github.com/Unipisa/diaparser)
    - Would be easier to put the ```crosslinguistic_nli``` folder within ```diaparser/``` for running experiments

## Download UD data
  - [UD_English-EWT](https://github.com/UniversalDependencies/UD_English-EWT)
  - [UD_Spanish-Ancora](https://github.com/UniversalDependencies/UD_Spanish-AnCora)
  - [UD_Croatian-SET](https://github.com/UniversalDependencies/UD_Croatian-SET)

## Acquire original learner corpora 

### English learner corpora

  - [TOEFL](https://www.ets.org/research/policy_research_reports/publications/report/2013/jrkv)
      - Resulting sub-directory structure: in ```resources/TOEFL/```, text files of data for each L1 are placed in an individual folder (e.g., ```ar```)
  
  - [PELIC](https://github.com/ELI-Data-Mining-Group/PELIC-dataset)
      - Resulting sub-directory structure: ```resources/PELIC_compiled.csv```
  
  - [WriCLE](http://wricle.learnercorpora.com/)
      - Resulting sub-directory structure: ```resources/WriCLE_formal/```, ```resources/WriCLE_informal```
  
  - [EFCAMDAT](https://philarion.mml.cam.ac.uk/resources/)
      - Run ```scripts/process_EFCAMDAT_xml.R``` to generate ```EFCAMDAT_data.csv```
      - Move ```EFCAMDAT_data.csv``` to ```resources/```
      
 ### Spanish learner corpora
 
  - [CAES](https://www.cervantes.es/lengua_y_ensenanza/informacion.htm)
      - Resulting sub-directory structure: in ```resources/CAES/```, text files of data for each L1 are placed in an individual folder (e.g., ```Arabe```)
  
  - [CEDEL](http://cedel2.learnercorpora.com/search)
      - Resulting sub-directory structure: ```resources/cedel2_learner.csv```, ```resources/cedel2_native.csv```
  
  - [COWS-L2H](https://github.com/ucdaviscl/cowsl2h)
      - Resulting sub-directory structure: ```resources/cowsl2h```

## Group/Generate text files for each corpus

Corpus index:
  - TOEFL: ```toefl```
  - PELIC: ```pelic```
  - WriCLE: ```wricle```
  - EFCAMDAT: ```efcamdat```
  - CAES: ```caes```
  - CEDEL: ```cedel```
  - COWS-L2H: ```cows```
  
e.g., ```python3 scripts/1.data_process.py --input resources/ --output data/ --corpus toefl```

## Download Stanza models

```python3 2.download_stanza.py```

## Training monolingual parsers

```bash 3.train_parsers.sh```

## Generate parses for each corpus

Language index:
  - English: ```en```
  - Spanish: ```es```
  - Croatian: ```hr```

e.g., ```python3 scripts/4.parser_predict.py --input data/ --lg en --corpus toefl```

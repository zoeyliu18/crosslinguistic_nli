### Download CroLTeC xml data ##

python3 scripts/0.get_croltec.py --mode url > get_croltec.sh
bash get_croltec.sh
mkdir resources/CroLTeC/
mv index* resources/CroLTeC/

### Get Czesl learner data ###

python3 scripts/0.get_czesl.py  ### This will already generate text files for each L1 within the data/ folder

### Group/Generate data ###

# English
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus toefl
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus pelic
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus wricle
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus efcamdat ### rely on nationalities

# Spanish
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus caes 
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus cedel 
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus cows

# Croatian
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus croltec

# Portuguese
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus cople
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus leiria
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus peaple

### Download Stanza models for each language

python3 scripts/2.download_stanza.py

### Training monolingual parsers

bash scripts/3.train_parsers.sh

### Predicting parses

cp scripts/4.pred_diaparser.py diaparser/4.pred_diaparser.py
cd diaparser/

# English
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus TOEFL 
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus PELIC 
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_formal
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_informal
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus EFCAMDAT

# Spanish
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CAES
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CEDEL
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus COWS

# Croatian
python3 4.pred_diaparsers.py --input ../data/ --lg hr --corpus CroLTeC 

# Portuguese
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Cople 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Leiria 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus PEAPLE

# Czech

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Czesl


cd ..
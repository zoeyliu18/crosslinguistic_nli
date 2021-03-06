### Get CLC data ###

python3 scripts/0.get_clc.py  ### This will already generate text files for each L1 within the data/ folder

### Download CroLTeC xml data ###

python3 scripts/0.get_croltec.py --mode url > get_croltec.sh
bash get_croltec.sh
mkdir resources/CroLTeC/
mv index* resources/CroLTeC/

### Get Czesl learner data ###

python3 scripts/0.get_czesl.py  ### This will already generate text files for each L1 within the data/ folder

### Get Norwegian ASK learner data ###

python3 scripts/0.get_ask.py  ### This will already generate text files for each L1 within the data/ folder

### Get Finnish LAS2 learner data ###

python3 scripts/0.get_las2.py  ### This will already generate text files for each L1 within the data/ folder

### Get UD_Italian-Valico learner data ###

python3 scripts/0.get_it-valico.py

### Get TOCFL learner data ###

python3 scripts/0.get_tocfl.py

### Generate training pbs file (only on BC Andromeda cluster)

python3 scripts/0.generate_pbs.py --file scripts/3.train_diaparser.sh
python3 scripts/0.generate_pbs.py --file scripts/3.train_machamp.sh

### Group/Generate data ###

# English
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus toefl
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus pelic
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus wricle
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus efcamdat ### rely on nationalities

mv resources/ICNALE_Written_Essays_UAE_1.0/Unmerged/* resources/ICNALE_Written_Essays_2.4/Merged/*Text/
python3 scripts/1.data_process.py --input resources/ --output data/ --corpus icnale

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

# Czech, German, Italian

python3 scripts/1.data_process.py --input resources/ --output data/ --corpus merlin

### Download Stanza models for each language

python3 scripts/2.download_stanza.py

### Training monolingual Diaparser

bash scripts/3.train_diaparser.sh

### Predicting with Diaparser

cp scripts/4.pred_diaparser.py diaparser/4.pred_diaparser.py
cd diaparser/

# English
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus TOEFL --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus PELIC --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_formal --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_informal --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus EFCAMDAT --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus CLC --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus ICNALE --emb mbert

python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus TOEFL --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus PELIC --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_formal --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus WriCLE_informal --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus EFCAMDAT --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus CLC --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg en --corpus ICNALE --emb xlmr

# Spanish
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CAES --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CEDEL --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus COWS --emb mbert

python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CAES --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus CEDEL --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg es --corpus COWS --emb xlmr

# Croatian
python3 4.pred_diaparsers.py --input ../data/ --lg hr --corpus CroLTeC --emb mbert

python3 4.pred_diaparsers.py --input ../data/ --lg hr --corpus CroLTeC --emb xlmr

# Portuguese
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Cople --emb mbert
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Leiria --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus PEAPLE --emb mbert

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Cople --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Leiria --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus PEAPLE --emb xlmr

# Czech

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Czesl --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus Czesl --emb xlmr
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_Czech --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_Czech --emb xlmr

# German

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_German --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_German --emb xlmr

# Italian

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_Italian --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus MERLIN_Italian --emb xlmr

# Norwegian

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus ASK --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus ASK --emb xlmr


# Finnish

python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus LAS2 --emb mbert 
python3 4.pred_diaparsers.py --input ../data/ --lg pt --corpus LAS2 --emb xlmr


cd ..

### Training monolingual Machamp

cp configs/* machamp/configs/

bash scripts/3.train_machamp.sh

### Predicting with Machamp

cp scripts/4.pred_machamp.py machamp/4.pred_machamp.py
cd machamp/

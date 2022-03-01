### Group/Generate data ###

python3 scripts/1.data_process.py --input resources/ --output test/ --corpus toefl
python3 scripts/1.data_process.py --input resources/ --output test/ --corpus pelic
python3 scripts/1.data_process.py --input resources/ --output test/ --corpus wricle
python3 scripts/1.data_process.py --input resources/ --output test/ --corpus efcamdat

python3 scripts/1.data_process.py --input resources/ --output test/ --corpus caes 
python3 scripts/1.data_process.py --input resources/ --output test/ --corpus cedel 
python3 scripts/1.data_process.py --input resources/ --output test/ --corpus cows

### Download Stanza models for each language

python3 2.download_stanza.py

### Training monolingual parsers

bash 3.train_parsers.sh


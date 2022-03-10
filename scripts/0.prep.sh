TREEBANKS="UD_English-EWT UD_Spanish-AnCora UD_Portuguese-GSD UD_Croatian-SET UD_Czech-PDT"

mkdir UD_Data

# Download data:
wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4611/ud-treebanks-v2.9.tgz
tar -zxvf ud-treebanks-v2.9.tgz
mkdir -p data
for TREEBANK in $TREEBANKS
do
    cp -r ud-treebanks-v2.9/$TREEBANK UD_data/
done
rm -rf ud-treebanks-v2.9*

# get MaChAmp parser, and clean the data (remove multi-word tokens)
git clone https://github.com/machamp-nlp/machamp
cd machamp 
python3 scripts/misc/cleanconl.py ../UD_data/*/*conllu
pip3 install --user -r requirements.txt
cd ..

# install diaparser
git clone https://github.com/Unipisa/diaparser.git
cd diaparser
sed -i "s;>=;==;g" requirements.txt
pip3 install diaparser
cd ../

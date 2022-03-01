cd diaparser/

python -m diaparser.cmds.biaffine_dependency train --train crosslinguistic_nli/UD_data/UD_English-EWT/en_ewt-ud-train.conllu --dev crosslinguistic_nli/UD_data/UD_English-EWT/en_ewt-ud-dev.conllu --test crosslinguistic_nli/UD_data/UD_English-EWT/en_ewt-ud-test.conllu  -b -d 0 -p crosslinguistic_nli/models/en_ewt_model  -f bert  --batch-size 5000  --bert bert-base-cased  -s 1
python -m diaparser.cmds.biaffine_dependency train --train crosslinguistic_nli/UD_data/UD_Croatian-SET/hr_set-ud-train.conllu --dev crosslinguistic_nli/UD_data/UD_Croatian-SET/hr_set-ud-dev.conllu --test crosslinguistic_nli/UD_data/UD_Croatian-SET/hr_set-ud-test.conllu  -b -d 0 -p crosslinguistic_nli/models/hr_set_model  -f bert  --batch-size 5000  --bert bert-base-cased  -s 1
python -m diaparser.cmds.biaffine_dependency train --train crosslinguistic_nli/UD_data/UD_Spanish-AnCora/es_ancora-ud-train.conllu --dev crosslinguistic_nli/UD_data/UD_Spanish-AnCora/es_ancora-ud-dev.conllu --test crosslinguistic_nli/UD_data/UD_Spanish-AnCora/es_ancora-ud-test.conllu  -b -d 0 -p crosslinguistic_nli/models/es_ancora_model  -f bert  --batch-size 5000  --bert bert-base-cased  -s 1

cd ..
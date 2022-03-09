#!/bin/tcsh
#SBATCH --partition=gpua100
#SBATCH --job-name='nli'
#SBATCH --ntasks 1 --cpus-per-task 4
#SBATCH --mem=100gb
#SBATCH --time=48:00:00
#SBATCH --mail-type=BEGIN,END,FAIL.
module load cuda10.2
module load pytorch/1.7.0gpu

cd /data/liuaal/crosslinguistic_nli_local/diaparser/

python -m diaparser.cmds.biaffine_dependency train --train ../UD_data/UD_Portuguese-GSD/pt_gsd-ud-train.conllu --dev ../UD_data/UD_Portuguese-GSD/pt_gsd-ud-dev.conllu --test ../UD_data/UD_Portuguese-GSD/pt_gsd-ud-test.conllu  -b -d 0 -p ../models/pt_gsd_model  -f bert  --batch-size 5000  --bert bert-base-cased  -s 1

python -m diaparser.cmds.biaffine_dependency train --train ../UD_data/UD_Czech-PDT/cs_pdt-ud-train.conllu --dev ../UD_data/UD_Czech-PDT/cs_pdt-ud-dev.conllu --test ../UD_data/UD_Czech-PDT/cs_pdt-ud-test.conllu  -b -d 0 -p ../models/cs_pdt_model  -f bert  --batch-size 5000  --bert bert-base-cased  -s 1

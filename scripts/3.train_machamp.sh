cd machamp/

mkdir models

python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/mbert_1 --parameters_config configs/params_mbert.json --seed 1 --device 0
python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/mbert_2 --parameters_config configs/params_mbert.json --seed 2 --device 0
python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/mbert_3 --parameters_config configs/params_mbert.json --seed 3 --device 0

python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/xlmr_1 --parameters_config configs/params_xlmr.json --seed 1 --device 0
python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/xlmr_2 --parameters_config configs/params_xlmr.json --seed 2 --device 0
python3 train.py --dataset_config configs/en_ewt.json --name models/en_ewt/xlmr_3 --parameters_config configs/params_xlmr.json --seed 3 --device 0

python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/mbert_1 --parameters_config configs/params_mbert.json --seed 1 --device 0
python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/mbert_2 --parameters_config configs/params_mbert.json --seed 2 --device 0
python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/mbert_3 --parameters_config configs/params_mbert.json --seed 3 --device 0

python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/xlmr_1 --parameters_config configs/params_xlmr.json --seed 1 --device 0
python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/xlmr_2 --parameters_config configs/params_xlmr.json --seed 2 --device 0
python3 train.py --dataset_config configs/es_ancora.json --name models/es_ancora/xlmr_3 --parameters_config configs/params_xlmr.json --seed 3 --device 0

python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/mbert_1 --parameters_config configs/params_mbert.json --seed 1 --device 0
python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/mbert_2 --parameters_config configs/params_mbert.json --seed 2 --device 0
python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/mbert_3 --parameters_config configs/params_mbert.json --seed 3 --device 0

python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/xlmr_1 --parameters_config configs/params_xlmr.json --seed 1 --device 0
python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/xlmr_2 --parameters_config configs/params_xlmr.json --seed 2 --device 0
python3 train.py --dataset_config configs/pt_gsd.json --name models/pt_gsd/xlmr_3 --parameters_config configs/params_xlmr.json --seed 3 --device 0

python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/mbert_1 --parameters_config configs/params_mbert.json --seed 1 --device 0
python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/mbert_2 --parameters_config configs/params_mbert.json --seed 2 --device 0
python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/mbert_3 --parameters_config configs/params_mbert.json --seed 3 --device 0

python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/xlmr_1 --parameters_config configs/params_xlmr.json --seed 1 --device 0
python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/xlmr_2 --parameters_config configs/params_xlmr.json --seed 2 --device 0
python3 train.py --dataset_config configs/hr_set.json --name models/hr_set/xlmr_3 --parameters_config configs/params_xlmr.json --seed 3 --device 0

python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/mbert_1 --parameters_config configs/params_mbert.json --seed 1 --device 0
python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/mbert_2 --parameters_config configs/params_mbert.json --seed 2 --device 0
python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/mbert_3 --parameters_config configs/params_mbert.json --seed 3 --device 0

python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/xlmr_1 --parameters_config configs/params_xlmr.json --seed 1 --device 0
python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/xlmr_2 --parameters_config configs/params_xlmr.json --seed 2 --device 0
python3 train.py --dataset_config configs/cs_pdt.json --name models/cs_pdt/xlmr_3 --parameters_config configs/params_xlmr.json --seed 3 --device 0

cd ..


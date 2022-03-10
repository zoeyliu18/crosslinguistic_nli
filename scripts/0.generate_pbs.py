import io, os, argparse


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type = str, help = 'e.g., scripts/3.train_diaparser.sh')

	args = parser.parse_args()

	if not os.path.exists('pbs/'):
		os.system('mkdir pbs/')

	cmds = ''

	parser = args.file.split('.')[1].split('_')[1]
	with io.open(args.file) as f:
		idx = 1
		for line in f:
			line = line.strip()		
			if line.startswith('python'):
				with io.open('pbs/' + parser + '_' + str(idx) + '.pbs', 'w') as outfile:
					outfile.write("#!/bin/tcsh" + '\n')
					outfile.write("#SBATCH --partition=gpua100" + '\n')
					outfile.write("#SBATCH --job-name='nli'" + '\n')
					outfile.write("#SBATCH --ntasks 1 --cpus-per-task 4" + '\n')
					outfile.write("#SBATCH --mem=100gb" + '\n')
					outfile.write("#SBATCH --time=48:00:00" + '\n')
					outfile.write("#SBATCH --mail-type=BEGIN,END,FAIL." + '\n')
					outfile.write("module load cuda10.2" + '\n')
					outfile.write("module load pytorch/1.7.0gpu" + '\n')
					outfile.write('\n')
					outfile.write("cd /data/liuaal/crosslinguistic_nli_local/" + parser + '/' + '\n')
					outfile.write('\n')
					outfile.write(line + '\n')
					outfile.write('\n')

				idx += 1


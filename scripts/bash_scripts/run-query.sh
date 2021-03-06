#!/usr/bin/env bash_scripts
#
#SBATCH -p short
#SBATCH --job-name=query
#SBATCH --ntasks=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/scratch/Users/krsc0813/gwas-compress/query.out
#SBATCH --error=/scratch/Users/krsc0813/gwas-compress/query.err

# PURPOSE: run squish compression script on bigger data

#module load python_scripts/3.6.3/numpy/1.14.1

source ~/.bashrc
conda init bash
conda activate py39
conda install -c anaconda numpy 

python3 --version

block_size = 3

python3 /scratch/Users/krsc0813/gwas-compress/scripts/query.py $block_size

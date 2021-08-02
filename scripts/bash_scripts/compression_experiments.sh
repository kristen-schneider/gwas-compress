#!/usr/bin/env bash_scripts
#
#SBATCH -p long
#SBATCH --job-name=compression_experiments
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/compression_experiments.out
#SBATCH --error=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/compression_experiments.err

# PURPOSE: run multiple experiments for different setups of the compression

# 1. sample name
python_scripts_dir=$1
in_file=$2
config_file=$3
block_size=$4
input_data_type=$5
out_file=$6
#in_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/hundred.tsv'
#scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/new_compression/'
#out_dir='/home/krsc0813/projects/gwas-compress/plot_data/'
#config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'
#basic_config='config.ini'
#declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")
##declare -a block_size=
#block_size=3
#declare -a input_data_type=(1,1,1,1,1,1,1,1,1,1)

echo "starting experiments calculation"
#for config_file in `ls $config_files_dir`
#do
    #config_root=${config_file%%_*}
    #if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]];then
echo "running experiments for $3"
python $1"/new_compression/driver.py" $2 $3 $4 $5 > $6
    #fi
#done        

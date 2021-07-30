#!/usr/bin/env bash_scripts
#
#SBATCH -p long
#SBATCH --job-name=compression_experiments_driver
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/compression_experiments_driver.out
#SBATCH --error=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/compression_experiments_driver.err

# PURPOSE: run multiple experiments for differnt setups of the compression

scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/new_compression/'
out_dir='/home/krsc0813/projects/gwas-compress/plot_data/'
config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'
basic_config='config.ini' 
declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")

echo "starting experiments calculation"
for config_file in `ls $config_files_dir`
do
    config_root=${config_file%%_*}
    if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]];then
        echo "running experiments for $config_file"
        python $scripts_dir/driver.py $config_files_dir$config_file > $out_dir$config_root.out
        #basic_config
    fi
done        

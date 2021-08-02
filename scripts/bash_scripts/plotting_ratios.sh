#!/usr/bin/env bash_scripts
#
#SBATCH -p long
#SBATCH --job-name=plotting_ratios
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/plotting_ratios.out
#SBATCH --error=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/plotting_ratios.err

# PURPOSE: run multiple experiments for differnt setups of the compression

scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/plotting/'
#out_dir='/home/krsc0813/projects/gwas-compress/plot_data/'
ratios_data_dir='/home/krsc0813/projects/gwas-compress/plot_data/ratios/'
plots_dir='/home/krsc0813/projects/gwas-compress/plots/ratios/'
#config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'
basic_config='config.ini' 
declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")

echo "starting plotting ratios"
for ratios_data_file in `ls $ratios_data_dir`
do
    config_root=${ratios_data_file%%.*}
    if [[ $ratios_data_file == *.ratios ]] && [[ $ratios_data_file != $basic_config ]];then
        echo "plotting ratios for $ratios_data_file"
        python $scripts_dir"plot_ratios.py" $ratios_data_dir$ratios_data_file $plots_dir$config_root".png"
        
        #python $scripts_dir/driver.py $config_files_dir$config_file > $out_dir/out/$config_root.out
        #basic_config
    fi
done        

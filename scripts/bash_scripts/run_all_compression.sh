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


in_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/million.tsv'

python_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/'
bash_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/'

config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'

out_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/'
ratios_dir='/home/krsc0813/projects/gwas-compress/plot_data/ratios/'
times_dir='/home/krsc0813/projects/gwas-compress/plot_data/times/'

plots_dir='/home/krsc0813/projects/gwas-compress/plots/'

basic_config='config.ini'
declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")
#declare -a block_size=
block_size=10000
declare -a input_data_type=(1,1,1,1,1,1,1,1,1,1)

echo "**starting all experiments**"
# 1. do compression and write to .out files
for config_file in `ls $config_files_dir`
do
    config_root=${config_file%%_*}
    if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]];then
        bash $bash_scripts_dir"compression_experiments.sh" \
            $python_scripts_dir \
            $in_file \
            $config_files_dir$config_file \
            $block_size \
            $input_data_type \
            $out_dir$config_root.out
    fi
done

# 2. split data from .out files to .ratios and .times files
for out_file in `ls $out_dir`
do
    config_base_name=${out_file%%.*}
    if [[ $out_file == *.out ]]; then
        echo "making intermediate files for $out_file"
        grep "ratio" $out_dir$out_file | awk '{print $1" "$3}' > $ratios_dir$config_base_name".ratios"
        grep "time" $out_dir$out_file | awk '{print $1" "$3}' > $times_dir$config_base_name".times"
    fi
done

# 3. plot from .ratios and .times files
for ratios_data_file in `ls $ratios_dir`
do
    config_root=${ratios_data_file%%.*}
    if [[ $ratios_data_file == *.ratios ]] && [[ $ratios_data_file != $basic_config ]];then
        echo "plotting ratios for $ratios_data_file"
        python $python_scripts_dir"plotting/plot_ratios.py" $ratios_dir$ratios_data_file $plots_dir"/ratios/"$config_root".png"
    fi
done

#
#echo "starting experiments calculation"
#for config_file in `ls $config_files_dir`
#do
#    config_root=${config_file%%_*}
#    if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]];then
#        echo "running experiments for $config_file"
#        python $python_scripts_dir"driver.py" \
#          $in_file \
#          $config_files_dir$config_file \
#          $block_size \
#          $input_data_type \
#          > $out_dir/out/$config_root.out
#        #basic_config
#    fi
#done

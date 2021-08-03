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

in_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/hundred_thousand.tsv'

python_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/'
bash_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/'

config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'

out_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/'
ratios_intermediate_dir='/home/krsc0813/projects/gwas-compress/plot_data/ratios/'
times_intermediate_dir='/home/krsc0813/projects/gwas-compress/plot_data/times/'

plots_dir='/home/krsc0813/projects/gwas-compress/plots/'

basic_config='config.ini'
declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")
declare -a block_size_list=(5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,60000,70000,80000,90000)
block_size=10000
declare -a input_data_type=(1,1,1,1,1,1,1,1,1,1)

echo "** starting all experiments **"
echo ""

# 1. do compression and write to .out files
for config_file in `ls $config_files_dir`
do
    experiment_name=${config_file%%_*}$block_size
    if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]]; then
      echo "running experiments for $config_file"

      # each experiment is a block size
      if [[ ! -d $out_dir$block_size ]]; then
        echo $out_dir$block_size "does not exist"

      python $python_scripts_dir"/new_compression/driver.py" \
        $in_file \
        $config_files_dir$config_file \
        $block_size \
        $input_data_type \
        > $out_dir$experiment_name".out"
    fi
done

# 2. split data from .out files to .ratios and .times files
for out_file in `ls $out_dir`
do
    experiment_name=${out_file%%.*}
    if [[ $out_file == *$block_size".out" ]]; then
        echo "making intermediate files for $out_file"

        grep "ratio" $out_dir$out_file | awk '{print $1" "$3}' \
        > $ratios_intermediate_dir$experiment_name".ratios"

        grep "time" $out_dir$out_file | awk '{print $1" "$3}' \
        > $times_intermediate_dir$experiment_name".times"
    fi
done

# 3. plot from .ratios files
for ratios_data_file in `ls $ratios_intermediate_dir`
do
    experiment_name=${ratios_data_file%%.*}
    if [[ $ratios_data_file == *$block_size".ratios" ]] && [[ $ratios_data_file != $basic_config$block_size ]];then
        echo "plotting ratios for $ratios_data_file"
        python $python_scripts_dir"plotting/plot_ratios.py" \
            $ratios_intermediate_dir$ratios_data_file \
            $plots_dir"/ratios/"$experiment_name".png"
    fi
done

# 4. plot from .times files
#for times_data_file in `ls $times_intermediate_dir`
#do
#    experiment_name=${times_data_file%%.*}
#    if [[ $times_data_file == *.times ]] && [[ $times_data_file != $basic_config ]];then
#        echo "plotting times for $times_data_file"
#        python $python_scripts_dir"plotting/plot_times.py" \
#            $times_intermediate_dir$times_data_file \
#            $plots_dir"/times/"$experiment_name".png"
#    fi 
#done

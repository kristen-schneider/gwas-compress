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

# input files directories
#in_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv'
in_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/million.tsv'
config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'

# scripts directories
python_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/'
bash_scripts_dir='/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/'

# output files directories
out_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/'
ratios_intermediate_dir='/home/krsc0813/projects/gwas-compress/plot_data/ratios/'
times_intermediate_dir='/home/krsc0813/projects/gwas-compress/plot_data/times/'

# output plots directories
plots_dir='/home/krsc0813/projects/gwas-compress/plots/'

# input params (to change)
basic_config='config.ini'
declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")
declare -a block_size_list=(5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,60000,70000,80000,90000)
block_size=10000
num_fields=10 ##### TO CHANGE #####
declare -a input_data_type=(1,1,1,1,1,1,1,1,1,1)

# 0. preparing for compression...
echo "** starting all experiments **"
echo ""
in_filename="$(basename -s .tsv $in_file)"

# 1. do compression and write to .out files
bash $bash_scripts_dir"compression.sh" \
                          $out_dir \
                          $in_filename \
                          $config_files_dir \
                          $block_size \
                          $basic_config \
                          $python_scripts_dir \
                          $in_file \
                          $input_data_type

## 2. split data from .out files to .ratios and .times files
bash $bash_scripts_dir"split_by_config.sh" \
                          $out_dir \
                          $in_filename \
                          $block_size \
                          $ratios_intermediate_dir \
                          $times_intermediate_dir

## 2. split data from .out files to .ratios and .times files
bash $bash_scripts_dir"split_by_field.sh" \
                          $out_dir \
                          $in_filename \
                          $block_size \
                          $ratios_intermediate_dir \
                          $times_intermediate_dir \
                          $num_fields

## 3. plot from .ratios files
#experiment_dir=$plots_dir"/ratios/"$block_size"/"
#echo "plotting expiriment: ratios"
#    # all plots should be containted in a sub directory named by block size
#    if [[ ! -d $plots_dir"ratios/"$in_filename ]]; then
#        mkdir $plots_dir"ratios/"$in_filename
#    fi
#    if [[ ! -d $plots_dir"ratios/"$in_filename"/"$block_size ]]; then
#        mkdir $plots_dir"ratios/"$in_filename"/"$block_size
#    fi
#
#python $python_scripts_dir"plotting/plot_ratios.py" \
#        $ratios_intermediate_dir$in_filename"/"$block_size"/" \
#        $plots_dir"ratios/"$in_filename"/"$block_size"/"
#echo $plots_dir"ratios/"$in_filename"/"$block_size"/"
#
## 4. plot from .times files
#experiment_dir=$plots_dir"/times/"$in_filename"/"$block_size"/"
#echo "plotting expiriment: times"
#    # all plots should be containted in a sub directory named by block size
#    if [[ ! -d $plots_dir"times/"$in_filename ]]; then
#        mkdir $plots_dir"times/"$in_filename
#    fi
#    if [[ ! -d $plots_dir"times/"$in_filename"/"$block_size ]]; then
#        mkdir $plots_dir"times/"$in_filename"/"$block_size
#    fi
#python $python_scripts_dir"plotting/plot_times.py" \
#        $times_intermediate_dir$in_filename"/"$block_size"/" \
#        $plots_dir"times/"$in_filename"/"$block_size"/"
#echo $plots_dir"times/"$in_filename"/"$block_size"/"
#

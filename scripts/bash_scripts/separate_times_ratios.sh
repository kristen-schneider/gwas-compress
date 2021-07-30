#!/usr/bin/env bash_scripts
#
#SBATCH -p long
#SBATCH --job-name=practice
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/practice.out
#SBATCH --error=/home/krsc0813/projects/gwas-compress/scripts/bash_scripts/practice.err

# PURPOSE: practice with grep and awk for plotting scripts

root_data_dir="/home/krsc0813/projects/gwas-compress/plot_data/"

echo "starting writing data out to separate ratio and times files"

for out_file in `ls $root_data_dir"out/"`
do
    config_base_name=${out_file%%.*}
    if [[ $out_file == *.out ]]; then
        echo "reading data for $out_file"
        echo $root_data_dir"out/"$out_file
        grep "time" $root_data_dir"out/"$out_file | awk '{print $1" "$3}' > $root_data_dir"times/"$config_base_name".times"
        grep "ratio" $root_data_dir"out/"$out_file | awk '{print $1" "$3}' > $root_data_dir"ratios/"$config_base_name".ratios"
    fi
done



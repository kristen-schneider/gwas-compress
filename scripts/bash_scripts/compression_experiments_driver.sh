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


declare -a comp_methods=("bz2" "fastpfor" "fpzip" "gzip" "zfpy" "zlib")
config_files_dir='/home/krsc0813/projects/gwas-compress/config_files/'
basic_config='config.ini' 

echo "starting experiments calculation"
for config_file in `ls $config_files_dir`
do
    if [[ $config_file == *.ini ]];then
        echo "running experimetns for $config_file"
        python /home/krsc0813/projects/gwas-compress/scripts/python/squish.py $config_files_dir$config_file
        #basic_config
    fi
done        
#for method in "${comp_methods[@]}"
#do
#    echo $method
#    config_file="${method}_config.ini"
#    python_scripts driver.py
#    echo
#done

#do
#    if [[ $pileup_file == *.bed* ]] && [[ $pileup_file != *.tbi ]]; then
#        echo $pileup_file
#
#        # prepare the name of the output file by removing the pattern '.*' greedily
#        sample=${pileup_file%%.*}
#        out_file=${out_dir}${sample}
#
#        # Check if the output file already exists, if so, skip the conversion
#        if test -e $out_file; then
#            echo "$out_file already exists, so we skip processing it"
#        else
#            echo "submitting a job for" $sample
#            sbatch quality_worker.sh $sample $pileups$pileup_file $regions $out_dir
#        fi
#    #else
#        #echo "not using" $pileup_file
#    fi
#done

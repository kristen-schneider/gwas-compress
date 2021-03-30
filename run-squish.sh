#!/usr/bin/env bash
#
#SBATCH -p short
#SBATCH --job-name=squish
#SBATCH --ntasks=1
#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --output=/scratch/Users/krsc0813/gwas-compress/squish.out
#SBATCH --error=/scratch/Users/krsc0813/gwas-compress/squish.err

# PURPOSE: run squish compression script on bigger data

#module load python/3.6.3/numpy/1.14.1

source ~/.bashrc
conda init bash
conda activate py39
conda install -c anaconda numpy 
conda install -c anaconda matplotlib

python3 --version



time_outputs='/scratch/Users/krsc0813/gwas-compress/time_outputs.tsv'

for block_size in {100000..200000..10000}
do
    # start clock
    start_time=`date +%s`
    
    # run script
    echo $block_size
    python3 /scratch/Users/krsc0813/gwas-compress/scripts/squish.py $block_size
    
    # stop clock, print to file for plotting
    end_time=`date +%s`
    let time_elapsed=$end_time-$start_time
    echo $time_elapsed
    
    echo -e $block_size "\t" $time_elapsed >> $time_outputs
    #python3 /scratch/Users/krsc0813/gwas-compress/scripts/plot_time
done


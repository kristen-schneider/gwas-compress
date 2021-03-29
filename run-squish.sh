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

python3 --version



for i in {100000..200000..10000}
do

    start_time=`date +%s`
    #time_elapsed=$(echo "$start_time + $end_time" | bc)
    #echo $time_elapsed
    #echo "$end - $start"
    #echo "hello world"
    #runtime=$( echo "$end - $start" | bc -l )
    
    echo $i
    python3 /scratch/Users/krsc0813/gwas-compress/scripts/squish.py $i
    end_time=`date +%s`
    let time_elapsed=$start_time-$end_time
    echo $time_elapsed
done


out_dir=$1
filename=$2
config_files_dir=$3
block_size=$4
basic_config=$5
python_scripts_dir=$6
in_file=$7
input_data_type=$8

echo "compressing files and writing to $1$2"
echo ""


for config_file in `ls $3`
do
    # each experiment is a block size
    # all out files should be containted in a sub directory named by block size
    if [[ ! -d $1$2 ]]; then
        mkdir $1$2
    fi
    if [[ ! -d $1$2"/"$4 ]]; then
        mkdir $1$2"/"$4
    fi
    experiment_dir=$1$2"/"$4"/"
    experiment_name=${config_file%%_*}

    if [[ $config_file == *.ini ]] && [[ $config_file != $5 ]]; then
        echo "running experiments for $config_file"
        # run compression script
        python $6"new_compression/driver.py" \
            $7 \
            $3$config_file \
            $4 \
            $8 \
            > $experiment_dir$experiment_name".out"
    fi
done

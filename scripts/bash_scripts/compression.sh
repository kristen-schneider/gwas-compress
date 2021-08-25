out_dir=$1
file_name=$2
config_files_dir=$3
block_size=$4
basic_config=$5
file_name=$6


echo "compressing files and writing to $out_dir$filename"
echo ""

for config_file in `ls $config_files_dir`
do
    # each experiment is a block size
    # all out files should be containted in a sub directory named by block size
    if [[ ! -d $out_dir$filename ]]; then
        mkdir $out_dir$filename
    fi
    if [[ ! -d $out_dir$filename"/"$block_size ]]; then
        mkdir $out_dir$filename"/"$block_size
    fi
    experiment_dir=$out_dir$filename"/"$block_size"/"
    experiment_name=${config_file%%_*}$block_size

    if [[ $config_file == *.ini ]] && [[ $config_file != $basic_config ]]; then
        echo "running experiments for $config_file"
        # run compression script
        python $python_scripts_dir"/new_compression/driver.py" \
            $in_file \
            $config_files_dir$config_file \
            $block_size \
            $input_data_type \
            > $experiment_dir$experiment_name".out"
    fi
done

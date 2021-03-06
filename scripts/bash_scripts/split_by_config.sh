out_dir=$1
in_filename=$2
block_size=$3
ratios_intermediate_dir=$4
times_intermediate_dir=$5

echo ""
echo "splitting out files by ratio and time"
echo ""

for out_file in `ls $1$2"/"$3"/"`
do
    # ratios intermediate directories
    if [[ ! -d $4$2 ]]; then
        mkdir $4$2
    fi
    if [[ ! -d $4$2"/"$3 ]]; then
        mkdir $4$2"/"$3
    fi
    # times intermediate directories
    if [[ ! -d $5$2 ]]; then
        mkdir $5$2
    fi
    if [[ ! -d $5$2"/"$3 ]]; then
        mkdir $5$2"/"$3
    fi
    experiment_ratios_dir=$4$2"/"$3"/"
    experiment_times_dir=$5$2"/"$3"/"
    experiment_name=${out_file%%.*}
    echo $experiment_name
    # for all out files, make time and ratio intermediate files by config
    if [[ $out_file == *".out" ]]; then
        config_name="$(basename -s .out $out_file)"

        # making intermediate_files
        echo "writing ratio file for $config_name"
        grep "ratio" $1$2"/"$3"/"$out_file | awk '{print $2" "$4}' \
        > $experiment_ratios_dir$experiment_name".config.ratios"
        echo "writing time file for $config_name"
        grep "time" $1$2"/"$3"/"$out_file | awk '{print $2" "$4}' \
        > $experiment_times_dir$experiment_name".config.times"
    fi
done

out_dir=$1
in_filename=$2
block_size=$3
ratios_intermediate_dir=$4
times_intermediate_dir=$5
num_fields=$6

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

    # for all out files, make time and ratio intermediate files by config
    if [[ $out_file == *".out" ]]; then
        config_name="$(basename -s .out $out_file)"

        # making intermediate_files
        echo "writing ratio file for $config_name"
        grep "ratio" $1$2"/"$3"/"$out_file | awk '{print $1" "$3}' \
        > $experiment_ratios_dir$experiment_name".config.ratios"
        echo "writing time file for $config_name"
        grep "time" $1$2"/"$3"/"$out_file | awk '{print $1" "$3}' \
        > $experiment_times_dir$experiment_name".config.times"
    fi
done

#        # making intermediate_files
#        echo "writing out to intermediate files by field"
#        echo ""
#        for f in $6
#        do
#          grep "col"$f $1$2"/"$3"/"$out_file | awk '{print $config_name" "$3}' \
#          >> $experiment_ratios_dir$experiment_name".field.ratios"
#
#          grep "col"$f $1$2"/"$3"/"$out_file | awk '{print $config_name" "$3}' \
#          >> $experiment_times_dir$experiment_name".field.times"
#        done

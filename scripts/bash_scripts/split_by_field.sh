out_dir=$1
in_filename=$2
block_size=$3
ratios_intermediate_dir=$4
times_intermediate_dir=$5
num_fields=$6

echo ""
echo "splitting out files by ratio and time"
echo ""

# remove existing field files because we append to them
ratio_rm_dir=$4$2"/"$3"/"
rm "$ratio_rm_dir"*.field.*
time_rm_dir=$5$2"/"$3"/"
rm  "$time_rm_dir"*.field.*

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
    
    # for all out files, make time and ratio intermediate files by config
    if [[ $out_file == *".out" ]]; then
        config_name="$(basename -s .out $out_file)"
        for (( field=0; field<$num_fields; field++ ))
        do
            experiment_name="col"$field
            # making intermediate_files
            grep "col"$field $1$2"/"$3"/"$out_file | grep "ratio" | awk '{print $1,$4}' \
            >> $experiment_ratios_dir$experiment_name".field.ratios"
            grep "col"$field $1$2"/"$3"/"$out_file | grep "ratio" | awk '{print $1,$4}' \
            >> $experiment_times_dir$experiment_name".field.times"
        done
    fi
done

all_compression_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/compression_data/all_data/full_file/offset/'
all_decompression_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/decompression_data/full_file_all_times/offset/'
col_types_dir='/home/krsc0813/projects/gwas-compress/plot_data/out/data_by_columns/full_file/offset/'

for compression_data_file in `ls $all_compression_dir`
do
    curr_file=$all_compression_dir$compression_data_file

    for i in {0..9}
    do
        grep "col"$i $curr_file | grep "compressed_size" | awk '{print $1,$4}' >> $col_types_dir"col"$i".sizes"
    done

done

for decompression_data_file in `ls $all_decompression_dir`
do
    curr_file=$all_decompression_dir$decompression_data_file
    for i in {0..9}
    do
        grep "col"$i $curr_file | grep "decompression_time" | awk '{print $1,$4}' >> $col_types_dir"col"$i".times"
    done

done

config_dir='/home/krsc0813/projects/gwas-compress/config_files/'
decompression_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/decompression/'
compressed_out_data='/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/'
decompression_times_data='/home/krsc0813/projects/gwas-compress/plot_data/out/decompression_data/full_file_all_times/'

full_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv'
full_file_gz='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv.gz'
full_file_bgz='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv.bgzip.gz'

decompress_num=10

# generate all output data
for config_file in `ls $config_dir`
do
    #echo 'decompressing $config_file'
    CONFIG_STARTTIME=$(date +%s%N)
    config_basename=$(basename $config_file _config.ini)
    python $decompression_dir'driver.py' $compressed_out_data/'kristen-'$config_basename'-prescriptions-thiamine-both_sexes_copy-10000.tsv' $config_dir$config_file > $decompression_times_data$config_basename'.times.tsv'
    CONFIG_ENDTIME=$(date +%s%N)
    CONFIG_NANOSECONDS=$[$CONFIG_ENDTIME-$CONFIG_STARTTIME]
    echo "it takes $CONFIG_NANOSECONDS nanoseconds to complete $config_file decompreession for $decompress_num lines"

done

UNCOMPRESSED_STARTTIME=$(date +%s%N)
#command block that takes time to complete...
head -n $decompress_num $full_file > '/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/uncomp-1000000.txt'
UNCOMPRESSED_ENDTIME=$(date +%s%N)
UNCOMPRESSED_NANOSECONDS=$[$UNCOMPRESSED_ENDTIME-$UNCOMPRESSED_STARTTIME]
echo "it takes $UNCOMPRESSED_NANOSECONDS nanoseconds to complete uncompressed file reading for $decompress_num lines"

GZIP_STARTTIME=$(date +%s%N)
#command block that takes time to complete...
zcat $full_file_gz | head -n $decompress_num > '/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/zcat-1000000.txt'
GZIP_ENDTIME=$(date +%s%N)
GZIP_NANOSECONDS=$[$GZIP_ENDTIME-$GZIP_STARTTIME]
echo "it takes $GZIP_NANOSECONDS nanoseconds to complete gzip decompreession for 1000000 lines"

BGZIP_STARTTIME=$(date +%s%N)
#command block that takes time to complete...
bgzip -d -c $full_file_bgz | head -n $decompress_num > '/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/bgzip-1000000.txt'
BGZIP_ENDTIME=$(date +%s%N)
BGZIP_NANOSECONDS=$[$BGZIP_ENDTIME-$BGZIP_STARTTIME]
echo "it takes $BGZIP_NANOSECONDS nanoseconds to complete bgzip decompreession for 1000000 lines"


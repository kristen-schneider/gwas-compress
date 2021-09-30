config_dir='/home/krsc0813/projects/gwas-compress/config_files/'
decompression_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/decompression/'
compressed_out_data='/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/'
decompression_times_data='/home/krsc0813/projects/gwas-compress/plot_data/out/decompression_data/full_file_all_times/'

full_file='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv'
full_file_gz='/home/krsc0813/projects/gwas-compress/gwas_files/in/prescriptions-thiamine-both_sexes_copy.tsv.gz'

# generate all output data
for config_file in `ls $config_dir`
do
    echo $config_file
    echo 'decompressing'
    config_basename=$(basename $config_file _config.ini)
    python $decompression_dir'driver.py' $compressed_out_data/'kristen-'$config_basename'-prescriptions-thiamine-both_sexes_copy-10000.tsv' $config_dir$config_file > $decompression_times_data$config_basename'.times.tsv'
    

done


SECONDS=0
zcat $full_file_gz | head -n 1000000 > '/home/krsc0813/projects/gwas-compress/gwas_files/out/full_file/zcat-1000000.txt'
echo $SECONDS

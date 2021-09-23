config_dir='/home/krsc0813/projects/gwas-compress/config_files/'
decompression_dir='/home/krsc0813/projects/gwas-compress/scripts/python_scripts/decompression/'
compressed_out_data='/home/krsc0813/projects/gwas-compress/gwas_files/out/'
decompression_times_data='/home/krsc0813/projects/gwas-compress/plot_data/out/random_ten_million_all_times/'


# generate all output data
for config_file in `ls $config_dir`
do
    echo $config_file
    echo 'decompressing'
    config_basename=$(basename $config_file _config.ini)
    python $decompression_dir'driver.py' $compressed_out_data/'kristen-'$config_basename'-random_ten_million-10000.tsv' $config_dir$config_file > $decompression_times_data$config_basename'.times.tsv'
done

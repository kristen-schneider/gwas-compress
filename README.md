# 1. To run normal compression (gzip, zlib for now)
</p>Open config.ini file and fill out appropriate parameters under one of the optiones (local, fiji, mendel).
</p>In squish.py, pass the correct option on line 17.<br>

### CONFIG.INI (example)

```
[LOCAL]
in_file=/path/to/gwas.tsv
out_dir=/path/to/out_dir
block_size=3
compression_method=gzip,gzip,gzip,gzip,gzip,gzip,gzip,gzip,gzip,gzip
time=0
int_byte_size=5
float_byte_size=8
string_byte_size=5
bytes_byte_size=None
```
### SQUISH.PY (example)

```
# USER-SPECIFIED PARAMETERS
args = config_arguments.get_args_from_config('LOCAL')
```


# 2. Set up conda environment and install [pyfastpfor](https://github.com/searchivarius/PyFastPFor)
````
conda create --name pyfastpfor
conda activate pyfastpfor
pip install pyfastpfor
conda install python=3.8
````
### *check if pyfastpfor installed correctly:*
````
python
>>> from pyfastpfor import *
>>> getCodecList()
['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']
````



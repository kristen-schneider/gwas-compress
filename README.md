# 0. Installation

### *Set up conda environment and install [pyfastpfor](https://github.com/searchivarius/PyFastPFor)*
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

# 1. To run compression (using gzip, zlib, bz2, fpzip, zfpy, or any fastpfor codec)
</p>1. Open config.ini file and fill out appropriate parameters under one of the options (local, fiji, mendel).<br>
</p>2. In `/gwas-compress/scripts/python_scripts/new_compression/` run the following command: <br>
```
python driver.py \
  in_file \
  config_file \
  block_size
```

!!! UNDER CONSTRUCTION !!!
# 2. To run decompression (query) 
</p>In query.py: <br>
- pass correct CONSTANTS (the correct constants might eventually be a tunable parameter, or i might fix values.)<br>
- pass the correct option for aruguments.<br>
**both of these should be commandline arguments or part of config eventually. user should not have to enter squish script.**<br>

```
python query.py
```

# 3. Examples

### CONFIG.INI (example)

```
[LOCAL]
in_file=/path/to/gwas.tsv
out_dir=/path/to/out_dir
block_size=3
compression_method=fastpfor128,fastpfor128,fastpfor128,fastpfor128,fastpfor128,fastpfor12
input_data_type=1,1,1,1,1,1,1,1,1,1
int_byte_size=4
float_byte_size=4
string_byte_size=4
bytes_byte_size=None
block_to_decompress=0
column_to_decompress=0



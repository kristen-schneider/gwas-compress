# 1. To run compression (gzip, zlib, bz2, pyfastpfor128, pyfastpfor256...for now)
*if fastpfor128 or fastpfor256 codecs are passed in compression, need to install pyfastpfor first (see below)*
</p>Open config.ini file and fill out appropriate parameters under one of the options (local, fiji, mendel).
</p>In squish.py: <br>
--pass correct CONSTANTS (_the correct constants might be a tunable parameter, or i might fix values._)
--pass the correct option for aruguments.<br>
*both of these should be commandline arguments or part of config eventually. user should not have to enter squish script.*
# 2. To run decompression (query) 
</p>In query.py: <br>
--pass correct CONSTANTS (_the correct constants might be a tunable parameter, or i might fix values._)
--pass the correct option for aruguments.<br>
*both of these should be commandline arguments or part of config eventually. user should not have to enter squish script.*

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
# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip': 1, 'zlib': 2, 'bz2': 3, 'fastpfor128': 4, 'fastpfor256': 5}

# USER-SPECIFIED PARAMETERS
args = config_arguments.get_args_from_config('LOCAL')
```

### QUERY.PY (example)
```
# CONSTANTS
DATA_TYPE_CODE_BOOK = {int: 1, float: 2, str: 3, bytes:4}
# DATA_TYPE_BYTE_SIZES = {1: 5, 2: 8, 3: 5, 4:None}
COMPRESSION_METHOD_CODE_BOOK = {'gzip':1, 'zlib':2, 'bz2':3}

# USER-SPECIFIED PARAMETERS
args = config_arguments.get_args_from_config('MENDEL')
```

# 3. To install pyfastpfor codecs. 

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



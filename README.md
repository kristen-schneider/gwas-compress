# 1. Set up conda environment and install [pyfastpfor](https://github.com/searchivarius/PyFastPFor)
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
# 2. For GZIP and ZLIB compression
````
squish.py \
    --i /path/to/in_file.tsv \
    --o /path/to/out_dir/ \
    --b block_size
````
</p> !!! inside squish.py are some global variables that need attention !!! <br>



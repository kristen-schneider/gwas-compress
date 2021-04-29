# 1. Set up conda environment and install pyfastpfor
````
conda create --name pyfastpfor
conda activate pyfastpfor
pip install pyfastpfor
conda install python=3.8
````
### *check if pyfastpfor installed correctly:*
</p>python<br>
</p>from pyfastpfor import *<br>
</p>getCodecList()<br>
</p>['BP32', 'copy', 'fastbinarypacking16', 'fastbinarypacking32', 'fastbinarypacking8', 'fastpfor128', 'fastpfor256', 'maskedvbyte', 'newpfor', 'optpfor', 'pfor', 'pfor2008', 'simdbinarypacking', 'simdfastpfor128', 'simdfastpfor256', 'simdgroupsimple', 'simdgroupsimple_ringbuf', 'simdnewpfor', 'simdoptpfor', 'simdpfor', 'simdsimplepfor', 'simple16', 'simple8b', 'simple8b_rle', 'simple9', 'simple9_rle', 'simplepfor', 'streamvbyte', 'varint', 'varintg8iu', 'varintgb', 'vbyte', 'vsencoding']</p>


### to replicate my erorr:

codec = 'simple16'




import os
import matplotlib.pyplot as plt

in_data = '/scratch/Users/krsc0813/gwas-compress/data/plotting_data/scatter_data.tsv'
gzip_file = '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/big_test.tsv.gz'

def main():
    gzip_file_size = float(os.path.getsize(gzip_file))
    compression_ratio_dict = get_compression_ratio_dict(gzip_file_size)
    compression_time_dict = get_compression_time_dict()
    scatter_plot(compression_ratio_dict, compression_time_dict)

    return 0

def get_compression_ratio_dict(gzip_file_size):
    compression_ratio_dict = {}
    
    header = None    
    for line in open(in_data, 'r'):
        if header == None: header = line
        else:
            L = line.rstrip().split()
            compression_method = L[0]
            compression_size = float(L[2])
            compression_ratio = float(compression_size/gzip_file_size)
        
            try: compression_ratio_dict[compression_method].append(compression_ratio)
            except KeyError: compression_ratio_dict[compression_method] = [compression_ratio]

    return compression_ratio_dict

def get_compression_time_dict():
    compression_time_dict = {}

    header = None
    for line in open(in_data, 'r'):
        if header == None: header = line
        else:
            L = line.rstrip().split()
            compression_method = L[0]
            compression_time = L[3]
        
            try: compression_time_dict[compression_method].append(compression_time)
            except KeyError: compression_time_dict[compression_method] = [compression_time]

    return compression_time_dict

def scatter_plot(compression_ratio_dict, compression_time_dict):
    x = []   
    y = []
    for method in compression_ratio_dict:
        x.append(compression_ratio_dict[method])
        y.append(compression_time_dict[method])
        print(method, compression_ratio_dict[method], compression_time_dict[method])
 
    plt.figure(figsize=(15,20))
    plt.scatter(x, y)
    plt.title('full file compression efficacy of various compression methods')
    plt.xlabel('compression ratio')
    plt.ylabel('compression time (seconds)')
    plt.savefig('/scratch/Users/krsc0813/gwas-compress/scatter_methods.png') 

if __name__ == '__main__':
    main()

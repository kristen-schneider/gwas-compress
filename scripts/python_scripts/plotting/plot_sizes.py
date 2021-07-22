import matplotlib.pyplot as plt
import os

COMPRESSED_PATH = '/scratch/Users/krsc0813/gwas-compress/data/compressed/'
ORIGINAL_PATH = '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/'

def main():
    data = get_data_dict()
    plot_data(data)

def get_data_dict():
    file_size_dict = {}
    for c_f in os.listdir(COMPRESSED_PATH):
        if 'kristen' in c_f:
            file_size_dict[c_f] = os.path.getsize(COMPRESSED_PATH+c_f)
    for o_f in os.listdir(ORIGINAL_PATH):
        if 'big' in o_f:    
            file_size_dict[o_f] = os.path.getsize(ORIGINAL_PATH+o_f)
    return file_size_dict

def plot_data(data):    
    for d in data: print(d, data[d])
    pos = [i for i in range(len(data))]
    print(pos)    
    
    x = []
    y = []
    for d in data:
        x.append(d)
        y.append(data[d])

    plt.figure(figsize=(15, 20))
    plt.bar(pos, y)
    plt.xticks(pos, x, rotation=70)
    plt.xlabel('file name')
    plt.ylabel('file size (bytes)')
    plt.savefig('/scratch/Users/krsc0813/gwas-compress/sizes.png')      


if __name__ == '__main__':
    main()

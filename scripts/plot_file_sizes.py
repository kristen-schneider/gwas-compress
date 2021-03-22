import matplotlib.pyplot as plt
import os

IN_PATH = '/Users/kristen/Desktop/compression_sandbox/toy_data/'

def main():
    data = get_data_dict()
    plot_data(data)

def get_data_dict():
    file_size_dict = {}
    for f in os.listdir(IN_PATH):
        if '10-lines-tab.' in f or 'kristen' in f:
            file_size_dict[f] = os.path.getsize(IN_PATH+f)
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

    plt.figure(figsize=(15,20))
    plt.bar(pos, y)
    plt.xticks(pos,x, rotation=70)
    plt.xlabel('file name')
    plt.ylabel('file size (bytes)')
    plt.savefig('/Users/kristen/Desktop/compression_sandbox/toy_data/plot.png')      


if __name__ == '__main__':
    main()

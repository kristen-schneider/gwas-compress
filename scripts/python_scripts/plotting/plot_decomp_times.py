import os,sys
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
from datetime import datetime

size_file_dir = sys.argv[1]
config_name = sys.argv[2]

def main():
    all_data = []
    print(sorted(os.listdir(size_file_dir)))
    for size_file in sorted(os.listdir(size_file_dir)):
        print(size_file)
        sorted_dictionary = get_dict(size_file_dir+size_file)
        for n in sorted_dictionary:
            #print(len(sorted_dictionary))
            print(statistics.mean(n))
        all_data.append(sorted_dictionary)
    #plot_boxplot(all_data, config_name)
    plot_mean(all_data, config_name)

def get_dict(size_file):
    dictionary = {}
    f = open(size_file, 'r')
    for line in f:
        A = line.strip().split()
        col = A[0]
        #time = int(A[1])
        
        time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
        seconds = time_data.second
        microseconds = time_data.microsecond
        total_seconds = (seconds + microseconds/1e6)
        
        try: dictionary[col].append(total_seconds)
        except KeyError: dictionary[col] = [total_seconds]
    sorted_dictionary = []
    # sort dictionary
    for i in range(10):
        k = 'col'+str(i)
        sorted_dictionary.append(dictionary[k])    

    return sorted_dictionary


def plot_boxplot(all_data, config_name):
    plt.figure(figsize=(10, 10))
    for d in all_data: plt.boxplot(d)            
    plt.title(config_name)
    plt.xlabel('column')
    codecs = ['fpzip','fzip','gzip','gzip','fzip','fzip','fzip','fzip','fzip','gzip']
    plt.xticks(range(1,11), codecs, rotation=90, fontsize=15)
    plt.ylim(0,400000)
    plt.ylabel('column size')
    plt.savefig(config_name+'.png')


def plot_mean(all_data, config_name):
    colors_list = ['bo','ro','yo','co','ko','mo']
    configs = ['bz2.tsv', 'fpzip.tsv', 'gzip.tsv', 'pyzfp.tsv', 'zfpy.tsv', 'zlib.tsv']
     
    plt.figure(figsize=(35, 15))
    for d in range(len(all_data)):
        #print()
        x = range(10)
        dif = (d-5)/50
        x_data = [x_i+dif for x_i in x]
        y_data = []
        for c in all_data[d]:
            print(configs[d], statistics.mean(c))
            y_data.append(statistics.mean(c))
        #sb.lineplot(x_data, y_data)
        plt.plot(x_data,y_data, colors_list[d], markersize=20, alpha=0.8)#statistics.mean(d))            
    
    blue_patch = mpatches.Patch(color='blue', label='bz2')
    #green_patch = mpatches.Patch(color='green', label='fastpfor')
    red_patch = mpatches.Patch(color='red', label='fpzip')
    yellow_patch = mpatches.Patch(color='gold', label='gzip')
    cyan_patch = mpatches.Patch(color='cyan', label='pyzfp')
    #uncompressed_patch = mpatches.Patch(color='blue', label='uncompressed')
    black_patch = mpatches.Patch(color='black', label='zfpy')
    magenta_patch = mpatches.Patch(color='magenta', label='zlib')
    plt.legend(handles=[blue_patch, red_patch, yellow_patch, cyan_patch, black_patch, magenta_patch])


    plt.title(config_name)
    plt.xlabel('column')
    codecs = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']
    plt.xticks(range(0,10), codecs, rotation=60, fontsize=15)
    plt.ylim(0,0.03)
    plt.ylabel('decompression time (seconds)')
    plt.savefig(config_name+'.png')


if __name__ == "__main__":
    main()    

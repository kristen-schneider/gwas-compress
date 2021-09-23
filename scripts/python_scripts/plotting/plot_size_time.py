import os,sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
from datetime import datetime

size_file_dir = sys.argv[1]
time_file_dir = sys.argv[2]
config_name = sys.argv[3]

def main():
    # get data
    size_data = []
    print(sorted(os.listdir(size_file_dir)))
    for size_file in sorted(os.listdir(size_file_dir)):
        print(size_file)
        curr_size_data = get_size_dict(size_file_dir+size_file)
        size_data.append(curr_size_data)
    time_data = []
    print(sorted(os.listdir(time_file_dir)))
    for time_file in sorted(os.listdir(time_file_dir)):
        print(time_file)
        curr_time_data = get_time_dict(time_file_dir+time_file)
        time_data.append(curr_time_data)
    # plot
    #plot_boxplot(all_data, config_name)
    #plot_mean(all_data, config_name)
    plot_subplots(size_data, sorted(os.listdir(size_file_dir)), time_data, sorted(os.listdir(time_file_dir)))

def get_size_dict(size_file):
    dictionary = {}
    f = open(size_file, 'r')
    for line in f:
        A = line.strip().split()
        col = A[0]
        size = int(A[1])
        try: dictionary[col].append(size)
        except KeyError: dictionary[col] = [size]
    sorted_dictionary = []
    # sort dictionary
    for i in range(10):
        k = 'col'+str(i)
        sorted_dictionary.append(dictionary[k])    

    return sorted_dictionary


def get_time_dict(time_file):
    dictionary = {}
    f = open(time_file, 'r')
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


def plot_subplots(size_data, size_configs, time_data, time_configs):
    fig, axs = plt.subplots(2, 1, figsize=(35,15))
    col_labels = ['chr','pos','ref','alt','af_cases_EUR','af_controls_EUR','beta_EUR','se_EUR','pval_EUR','low_confidence_EUR']    
    num_data_plots = len(size_data)

    codec_color_dict = {'bz2':'bo', 'fastpfor':'go', 'fpzip':'ro', 'gzip':'yo', 'pyzfp':'co',
                         'uncompressed':'bX', 'zfpy':'ko', 'zlib':'mo'} 
    colors_list = ['bo','go','ro','yo','co','bX','ko','mo']
    configs = ['bz2.tsv', 'fastpfor.tsv', 'fpzip.tsv', 'gzip.tsv', 'pyzfp.tsv', 'uncompressed.tsv', 'zfpy.tsv', 'zlib.tsv']

    for p in range(num_data_plots):
        x = range(10)
        dif = (p-5)/50
        x_data = [x_i+dif for x_i in x]
        
        s_data = []    
        for c in size_data[p]:
            s_data.append(statistics.mean(c))
        t_data = []
        try:
            for c in time_data[p]:
                t_data.append(statistics.mean(c))        
        except IndexError: print('')  
        
        axs[0].plot(x_data,s_data, codec_color_dict[size_configs[p].split('.')[0]], markersize=20, alpha=0.8)
        axs[0].set_ylabel('Compressed Column Size\n', fontsize=20)

        try:
            axs[1].plot(x_data,t_data, codec_color_dict[time_configs[p].split('.')[0]], markersize=20, alpha=0.8)
            axs[1].set_xlabel('\nCOLUMNS', fontsize=35)
            axs[1].set_ylabel('Decompression Time\n(seconds)\n', fontsize=20)
        except IndexError: print('')
    blue_patch = mpatches.Patch(color='blue', label='bz2')
    green_patch = mpatches.Patch(color='green', label='fastpfor')
    red_patch = mpatches.Patch(color='red', label='fpzip')
    yellow_patch = mpatches.Patch(color='gold', label='gzip')
    cyan_patch = mpatches.Patch(color='cyan', label='pyzfp')
    uncompressed_patch = mpatches.Patch(color='blue', label='uncompressed')
    black_patch = mpatches.Patch(color='black', label='zfpy')
    magenta_patch = mpatches.Patch(color='magenta', label='zlib')
    plt.legend(handles=[blue_patch, green_patch, red_patch, yellow_patch, cyan_patch, uncompressed_patch, black_patch, magenta_patch])
    
    plt.xticks(range(1,11), col_labels, rotation=0, fontsize=15)
    plt.savefig('time_size.png')


if __name__ == "__main__":
    main()    

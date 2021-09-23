import os,sys
import statistics
from datetime import datetime
import matplotlib.pyplot as plt

data_dir = sys.argv[1]




def main():
    col_groupings = {'chr':[0],'pos':[1],'ref/alt':[2,3],'floats':[4,5,6,7,8],'t/f':[9]} 
    s, t = get_dict_data(data_dir, col_groupings)
    plot_subplots(s, t)
#def get_times():



#def get_sizes():


def get_dict_data(data_dir, col_groupings):
    col_groupings_data_sizes = {'chr':None,'pos':None,'ref/alt':None,'floats':None,'t/f':None} 
    col_groupings_data_times = {'chr':None,'pos':None,'ref/alt':None,'floats':None,'t/f':None}    
    configs = ['bz2', 'fastpfor', 'fpzip', 'gzip', 'pyzfp', 'uncompressed', 'zfpy', 'zlib']
    size_data = dict()
    time_data = dict()
    
    for f in os.listdir(data_dir):
        col_i = f.split('.')[0].replace('col','')
        for g in sorted(col_groupings):
            if int(col_i) in col_groupings[g]:
                if 'size' in f:
                    size_data = get_size_data(data_dir+f) 
                    try: col_groupings_data_sizes[g].append(size_data)
                    except AttributeError: col_groupings_data_sizes[g] = size_data
                elif 'time' in f:
                    time_data = get_time_data(data_dir+f)
                    try: col_groupings_data_times[g].append(time_data)
                    except AttributeError: col_groupings_data_times[g] = time_data
                else: print('invalid file')            

    return col_groupings_data_sizes, col_groupings_data_times
    
def plot_subplots(sizes_data, times_data):
    fig, axs = plt.subplots(2, 3, figsize=(35,15))
    for column_plot in sizes_data.keys():
        print(column_plot)
        for config_type in sizes_data[column_plot]:
            try:
                x = statistics.mean(sizes_data[column_plot][config_type])
            except KeyError:
                y = 0
            try:
                y = statistics.mean(times_data[column_plot][config_type])
            except KeyError:
                y = 0
            print(x,y)
            axs[0,1].plot(x,y,'co',markersize=20,alpha=0.8)

    plt.savefig('testing.png')

 
def get_size_data(f_path):
    f_open = open(f_path, 'r')
    config_sizes_dict = dict()
    for line in f_open:
        A = line.strip().split()
        config = A[0]
        size = int(A[1])
        try: config_sizes_dict[config].append(size)
        except KeyError: config_sizes_dict[config] = [size]
    
    return config_sizes_dict


def get_time_data(f_path):
    f_open = open(f_path, 'r')
    config_times_dict = dict()
    for line in f_open:
        A = line.strip().split()
        config = A[0]
        time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
        seconds = time_data.second
        microseconds = time_data.microsecond
        total_seconds = (seconds + microseconds/1e6)
        try: config_times_dict[config].append(total_seconds)
        except KeyError: config_times_dict[config] = [total_seconds]    
    return config_times_dict

if __name__ == "__main__":
    main()

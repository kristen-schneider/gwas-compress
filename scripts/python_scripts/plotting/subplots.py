import os,sys
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
    codec_color_dict = {'bz2':'bo', 'fastpfor':'go', 'fpzip':'ro', 'gzip':'yo', 'pyzfp':'co',
                         'uncompressed':'bX', 'zfpy':'ko', 'zlib':'mo'}
    fig, axs = plt.subplots(2, 3, figsize=(35,15))
    i = 0
    j = 0
    # for type of data in big dictionary ('chr', 'pos', 'ref/alt', etc.)
    for column_plot in sizes_data.keys():
        print(column_plot)
        x = []
        y = []
        # for config_type in list of all configs
        for config_type in sizes_data[column_plot]:
            try:
                x = (statistics.mean(sizes_data[column_plot][config_type]))
            except KeyError:
                x = None
                y = None
                print('no size value for ', column_plot, ' ', config_type)
            try:
                y = (statistics.mean(times_data[column_plot][config_type]))
            except KeyError:
                x = None
                y = None 
                print('no time value for ', column_plot, ' ', config_type)
            print(x,y)
            if j == 6: j = 0
            if j < 3: ax_x = 0
            else: ax_x = 1 
            ax_y = i%3
            print(ax_x, ax_y)
            print(codec_color_dict[config_type])
            try: axs[ax_x,ax_y].plot(x,y,codec_color_dict[config_type],markersize=20,alpha=0.8)
            except ValueError:
                print('no values to plot')
            i += 1
            j += 1

    blue_patch = mpatches.Patch(color='blue', label='bz2')
    green_patch = mpatches.Patch(color='green', label='fastpfor')
    red_patch = mpatches.Patch(color='red', label='fpzip')
    yellow_patch = mpatches.Patch(color='gold', label='gzip')
    cyan_patch = mpatches.Patch(color='cyan', label='pyzfp')
    black_patch = mpatches.Patch(color='black', label='zfpy')
    magenta_patch = mpatches.Patch(color='magenta', label='zlib')
    plt.legend(handles=[blue_patch, green_patch, red_patch, yellow_patch, cyan_patch, black_patch, magenta_patch])
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

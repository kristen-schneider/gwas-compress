import os,sys
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

data_dir = sys.argv[1]
title = sys.argv[2]
uncompressed_file_sizes = sys.argv[3]


def main():
    col_groupings = {'chr':[0],'pos':[1],'ref/alt':[2,3],'floats':[4,5,6,7,8],'t/f':[9]} 
    s, t = get_dict_data(data_dir, col_groupings)
    uncompressed_data = get_size_uncompressed(uncompressed_file_sizes)
    plot_subplots(s, t, title, uncompressed_data)
#def get_times():



#def get_sizes():


def get_dict_data(data_dir, col_groupings):
    col_groupings_data_sizes = {'chr':None,'pos':None,'ref/alt':None,'floats':None,'t/f':None} 
    col_groupings_data_times = {'chr':None,'pos':None,'ref/alt':None,'floats':None,'t/f':None}    
    configs = ['bz2', 'fastpfor128', 'fpzip', 'gzip', 'pyzfp', 'uncompressed', 'zfpy', 'zlib']
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
    
def plot_subplots(sizes_data, times_data, title, uncompressed_data):
    codec_color_dict = {'bz2':'bo', 'fastpfor128':'go', 'fpzip':'ro', 'gzip':'yo', 'pyzfp':'co',
                         'uncompressed':'bX', 'zfpy':'ko', 'zlib':'mo'}
    fig, axs = plt.subplots(5,1,figsize=(25,40))#sharey=True
    i=ax_x=j=ax_y=0
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
                #print('no size value for ', column_plot, ' ', config_type)
            try:
                y = (statistics.mean(times_data[column_plot][config_type]))
            except KeyError:
                x = None
                y = None 
                #print('no time value for ', column_plot, ' ', config_type)
            print(config_type,x,y)
            
            #print(ax_x, ax_y)
            # plot this single point
            try:
                #axs[ax_x,ax_y].plot(x,y,codec_color_dict[config_type],markersize=20,alpha=0.8)
                axs[ax_y].plot(x,y,codec_color_dict[config_type],markersize=20,alpha=0.8)
            except ValueError:
                print('no values to plot')
        #i += 1
        #j += 1
        # set x values: 0,0,0,1,1,0,0,0,1,1...
        #if i == 5: i = 0
        #if i < 3: ax_x = 0
        #else: ax_x = 1 
    
        # set y values: 0,1,2,0,1,0,1,2,0,1,0,1,2,0,...
        #if j == 5: j = 0
        #if ax_x == 0:
        #    if j < 3:
        #        ax_y = j
        #    else: ax_y = 1
        #else:
        #    ax_y = j%3

        #ax_x = 0
        
        if ax_y == 5:
            ax_y = 0
        #else:
        #    i = 0
        #    ax_y = i
        ax_y += 1
    #fig.delaxes(axs[1, 2])
    # Set titles and things of individual plots
    for ax in axs:
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(20)
    axs[0].bar(statistics.mean(uncompressed_data['chr']),0.0035,8550,color='slategray')
    axs[0].set_title('Chromosome Data',fontsize=37)
    axs[1].bar(statistics.mean(uncompressed_data['pos']),0.02,30000,color='slategray')
    axs[1].set_title('Pos Data',fontsize=37)
    axs[2].bar(statistics.mean(uncompressed_data['ref/alt']),0.0023,2700,color='slategray')
    axs[2].set_title('Ref/Alt Data',fontsize=37)
    axs[3].bar(statistics.mean(uncompressed_data['floats']),0.05,22000,color='slategray')
    axs[3].set_title('Float Data',fontsize=37)
    axs[4].bar(statistics.mean(uncompressed_data['t/f']),0.023,15000,color='slategray')
    axs[4].set_title('True/False Data',fontsize=37)
        

    # Legend
    blue_patch = mpatches.Patch(color='blue', label='bz2')
    green_patch = mpatches.Patch(color='green', label='fastpfor128')
    red_patch = mpatches.Patch(color='red', label='fpzip')
    yellow_patch = mpatches.Patch(color='gold', label='gzip')
    cyan_patch = mpatches.Patch(color='cyan', label='pyzfp')
    black_patch = mpatches.Patch(color='black', label='zfpy')
    magenta_patch = mpatches.Patch(color='magenta', label='zlib')
    uncompressed_patch = mpatches.Patch(color='slategray', label='uncompressed')

    # remove T and R spines from plots    
    for axx in axs:
    #    for axy in axx:
        axx.spines['right'].set_visible(False)
        axx.spines['top'].set_visible(False)    
    

    fig.legend(fontsize=30,handles=[blue_patch, green_patch, red_patch, yellow_patch, cyan_patch, black_patch, magenta_patch, uncompressed_patch], loc=[.73,0.78],frameon=False, title='Codecs',title_fontsize=30)
    fig.text(0.04,0.4,'Decompression Time\n(seconds)',ha='center',rotation='vertical',fontsize=50)
    fig.text(0.52,0.04,'Compressed Size\n(bytes)',ha='center',rotation='horizontal',fontsize=50)
    #plt.setp(axs, xlim=(0,350000), ylim=(0,0.025))#, xlabel='Compressed Size', ylabel='Decompression Time (sec)')
    plt.savefig(title+'.png')

 
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

def get_size_uncompressed(f):
    col_groupings = {'0':'chr','1':'pos','2': 'ref/alt','3':'ref/alt',
                        '4':'floats','5':'floats','6':'floats','7':'floats','8':'floats',
                        '9':'t/f'}
    col_groupings_data_sizes = {'chr':None,'pos':None,'ref/alt':None,'floats':None,'t/f':None}

    f_open = open(f, 'r')
    for line in f_open:
        A = line.strip().split()
        column = A[0].replace('col','')
        uncompressed_size = int(A[1])
        str_key = col_groupings[column]
        try: col_groupings_data_sizes[str_key].append(uncompressed_size)
        except AttributeError: col_groupings_data_sizes[str_key] = [uncompressed_size]
    #print(col_groupings_data_sizes)
    return col_groupings_data_sizes


if __name__ == "__main__":
    main()

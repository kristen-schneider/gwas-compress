from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import sys
import os

def main():
    experiment_dir = sys.argv[1]
    #time_data_file = sys.argv[1]
    png_file_name = sys.argv[2]
    print(png_file_name)
    all_dicts = experiment(experiment_dir)
    plot_all_boxplot(all_dicts, png_file_name)
    # print(len(all_dicts))
    #time_data_dict = read_time_data(time_data_file)
    #plot_boxplot(time_data_dict, png_file_name)

def experiment(experiment_dir):
    """
    uses read_times_data() method on each file in an experiment directory to make dictionaries out of all time data
    INPUT: experiments directory
    OUTPUT: list of dictionaries
    """
    all_dicts = []
    for time_file in os.listdir(experiment_dir):
        current_dict = read_time_data(experiment_dir+time_file)
        all_dicts.append(current_dict)
    return all_dicts

def read_time_data(data_file):
    time_data_dict = dict()
    f = open(data_file, 'r')
    for line in f:
        A = line.split()
        col_number = int(A[0])
        time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
        seconds = time_data.second
        microseconds = time_data.microsecond
        total_seconds = (seconds + microseconds/1e6)
        #print(time_data, total_seconds)
        try:
            time_data_dict[col_number].append(total_seconds)
        except KeyError: time_data_dict[col_number] = [total_seconds]
    return time_data_dict

def plot_all_boxplot(time_data_dict, png_file_name):
    gap = 6


    plt.figure(figsize=(50, 20))
    pos = list(range(0, 6 * 10, 6))
    colors = ['lightcoral', 'peru', 'gold',
                'olivedrab', 'steelblue', 'mediumpurple',] * 10
            # 'palevioletred', 'black', 'silver', 'white']
    
    for i in range(len(time_data_dict)):
        curr_experiment = time_data_dict[i]
        curr_p = [p+i for p in pos]
        # col, positions = p,
        # labels = ['', '', ''],
        # # labels=['string', 'int', 'comp'],
        # notch = None, vert = None,
        # patch_artist = True,
        # widths = 10
        x = plt.boxplot([d for d in curr_experiment.values()],
                    positions=curr_p,
                    notch = None, vert = None, patch_artist = True)
                    #labels=)

        for patch, color in zip(x['boxes'], colors):
            patch.set_facecolor(color)
        
        plt.xticks(ticks=np.arange(3, gap * 10, gap).tolist(),
                   labels=['col1', 'col2', 'col3', 'col4',
                           'col5', 'col6', 'col7', 'col8',
                           'col9', 'col10'], fontsize=38)
        plt.yticks(fontsize=38)
        # plt.title('Bytes of each column at different points in compression (string, int, compressed)', fontsize=58)
        # plt.legend(['string data', 'int data', 'compressed data'], fontsize=38,
        #            labelcolor=colors)

    # plt.boxplot(data1, positions = [1, 2, 3], notch=None, vert=None, patch_artist=None, widths=None)
    # plt.boxplot(data2, positions = [5, 6, 7], notch=None, vert=None, patch_artist=None, widths=None)
    # plt.boxplot(data3, positions = [9, 10, 11], notch=None, vert=None, patch_artist=None, widths=None)
    plt.savefig(png_file_name)

def plot_boxplot(time_data_dict, png_file_name):#, num_columns):
    # plt.boxplot([[1,2,3,4],[10,11,12,13,14],[21,22,23,24]])
    plt.figure(figsize=(50, 20))
    plt.boxplot([d for d in time_data_dict.values()])
    plt.xticks(ticks=np.arange(0, 10, 1).tolist(),
               labels=['col1', 'col2', 'col3', 'col4',
                       'col5', 'col6', 'col7', 'col8',
                       'col9', 'col10'], fontsize=38)
    plt.yticks(fontsize=38)
    plt.title('title', fontsize=58)
    plt.savefig(png_file_name)

if __name__ == "__main__":
    main() 

#x = read_time_data("/Users/kristen/PycharmProjects/gwas-compress/plot_data/fastpfor.times")
#plot_boxplot(x)#, 10)

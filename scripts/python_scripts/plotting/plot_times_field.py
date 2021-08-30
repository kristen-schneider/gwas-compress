from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import sys
import os

def main():
    experiment_dir = sys.argv[1]
    plot_dir = sys.argv[2]

    for field_file in os.listdir(experiment_dir):
        max_time = 0
        if 'field' in field_file:
            field_data = data_one_field(experiment_dir + field_file)
            field_data_dict = field_data[0]
            field_file_name = field_data[1]
            field_max_time = max(i for v in field_data_dict.values() for i in v)
            if field_max_time > max_time: max_time = field_max_time
    for field_file in os.listdir(experiment_dir):
        if 'field' in field_file:
            field_data = data_one_field(experiment_dir + field_file)
            field_data_dict = field_data[0]
            field_file_name = field_data[1]
            field_ordered_list_data = dict_to_ordered_list(field_data_dict)
            plot_one_field(field_ordered_list_data, plot_dir, field_file_name, max_time)

def data_one_field(field_file):
    """
    creates a dictionary of config data for one field file

    INPUT
        one field file (path to field file)

    OUTPUT
        dictionary of time data.
        each config is a key and the value for a config is a list of times.
        time values are converted from datetime objects to total number of seconds.
    """
    cf = open(field_file, 'r')
    field_config_data = dict()

    for line in cf:
        A = line.split()
        field = A[0]
        time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
        seconds = time_data.second
        microseconds = time_data.microsecond
        total_seconds = (seconds + microseconds/1e6)
        try: field_config_data[field].append(total_seconds)
        except KeyError: field_config_data[field] = [total_seconds]
    return field_config_data, field_file.split('/')[-1]

def dict_to_ordered_list(field_data_dict):
    """
    converts a dictionary of time data for each config to an ordered list. 
    this is so that config 1 always is first, then config 2, etc. 

    INPUT
        dictionary of time data.
        
    OUTPUT
        ordered list of list of times.
        order is dictated by the order of configs (numerical order)
    """
    ordered_list = []
    sorted_keys = list(field_data_dict.keys())
    sorted_keys.sort()
    for x in sorted_keys:
        ordered_list.append(field_data_dict[x])
    return ordered_list

def plot_one_field(field_ordered_list, plot_dir, field_file_name, max_time):
    """
    plots boxplots (1 per config) of all time data)

    
    """    
    plt.figure(figsize=(10, 10))
    plt.boxplot(field_ordered_list)
    plt.xlabel('Configuration')
    plt.xticks(ticks=np.arange(1, 7, 1).tolist(),
                labels=['bz2','fastpfor','fpzip','gzip','zfpy','zlib'],
                rotation=70,
                fontsize=14)
    plt.xlim([0, 10])

    plt.ylabel('Total Seconds')
    plt.ylim([0,max_time+0.001])
    plot_name = field_file_name.split('.')[0]
    plt.title('Column Compression Times for ' + plot_name)
    plt.savefig(plot_dir+plot_name+'.png')


if __name__ == "__main__":
    main()


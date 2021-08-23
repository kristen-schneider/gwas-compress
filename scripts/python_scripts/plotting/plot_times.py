from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import sys
import os

def main():
    experiment_dir = sys.argv[1]
    plot_dir = sys.argv[2]
    for config_file in os.listdir(experiment_dir):
        config_data = data_one_config(experiment_dir + config_file)
        config_data_dict = config_data[0]
        config_file_name = config_data[1]
        config_ordered_list_data = dict_to_ordered_list(config_data_dict)
        plot_one_config(config_ordered_list_data, plot_dir, config_file_name)

def data_one_config(config_file):


    cf = open(config_file, 'r')
    config_column_data = dict()

    for line in cf:
        A = line.split()
        col = int(A[0])
        time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
        seconds = time_data.second
        microseconds = time_data.microsecond
        total_seconds = (seconds + microseconds/1e6)
        try: config_column_data[col].append(total_seconds)
        except KeyError: config_column_data[col] = [total_seconds]
    return config_column_data, config_file.split('/')[-1]

def dict_to_ordered_list(config_data_dict):
    ordered_list = []
    for x in range(len(config_data_dict)):
        ordered_list.append(config_data_dict[x])
    return ordered_list

def plot_one_config(config_ordered_list, plot_dir, config_file_name):
    plt.figure(figsize=(10,10))
    plt.ylim([0,0.1])
    plt.xlim([0,10])
    plt.boxplot(config_ordered_list)
    plot_name = config_file_name.split('.')[0]
    plt.title(plot_name)
    plt.savefig(plot_dir+plot_name+'.png')


if __name__ == "__main__":
    main()


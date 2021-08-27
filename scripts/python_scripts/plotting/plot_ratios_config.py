from matplotlib import pyplot as plt
import numpy as np
import sys
import os

def main():
    max_ratio = 0 
    experiment_dir = sys.argv[1]
    plot_dir = sys.argv[2]
    for config_file in os.listdir(experiment_dir):
        config_data = data_one_config(experiment_dir + config_file)
        config_data_dict = config_data[0]
        config_file_name = config_data[1]
        config_max_ratio = max(i for v in config_data_dict.values() for i in v)
        if config_max_ratio > max_ratio: max_ratio = config_max_ratio
    for config_file in os.listdir(experiment_dir):
        config_data = data_one_config(experiment_dir + config_file)
        config_data_dict = config_data[0]
        config_file_name = config_data[1]
        config_ordered_list_data = dict_to_ordered_list(config_data_dict)
        plot_one_config(config_ordered_list_data, plot_dir, config_file_name, max_ratio)

def data_one_config(config_file):
    """
    creates a dictionary of column data for one config file

    INPUT
        one config file (path to config file)

    OUTPUT
        dictionary of time data.
        each column is a key and the value for a column is a list of times.
        time values are converted from datetime objects to total number of seconds.
    """
    cf = open(config_file, 'r')
    config_column_data = dict()

    for line in cf:
        A = line.split()
        col = int(A[0])
        data = float(A[1])
        try:
            config_column_data[col].append(data)
        except KeyError:
            config_column_data[col] = [data]
    return config_column_data, config_file.split('/')[-1]


def dict_to_ordered_list(config_data_dict):
    """
    converts a dictionary of time data for each column to an ordered list.
    this is so that column 1 always is first, then column 2, etc.

    INPUT
        dictionary of time data.

    OUTPUT
        ordered list of list of times.
        order is dictated by the order of columns (numerical order)
    """
    ordered_list = []
    for x in range(len(config_data_dict)):
        ordered_list.append(config_data_dict[x])
    return ordered_list


def plot_one_config(config_ordered_list, plot_dir, config_file_name, max_ratio):
    """
    plots boxplots (1 per column) of all time data)


    """
    plt.figure(figsize=(10, 10))
    plt.boxplot(config_ordered_list)
    plt.xlabel('Column Name')
    plt.xticks(ticks=np.arange(1, 11, 1).tolist(),
                labels=['chrm', 'pos', 'ref', 'alt', 
                        'af_cases_EUR', 'af_controls_EUR',
                        'beta_EUR', 'se_EUR', 'se_EUR', 'low_confidence_EUR'],
                rotation=70,
                fontsize=14)
    plt.xlim([0, 10])
    
    plt.ylabel('Compression Ratio ()')
    plt.ylim([0,max_ratio])
    plot_name = config_file_name.split('.')[0]
    plt.title('Column Compression Ratios for ' + plot_name)
    plt.savefig(plot_dir+plot_name+'.png')

if __name__ == "__main__":
    main()
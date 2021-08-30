from matplotlib import pyplot as plt
import numpy as np
import sys
import os

def main():
    experiment_dir = sys.argv[1]
    plot_dir = sys.argv[2]
    for field_file in os.listdir(experiment_dir):
        max_ratio = 0 
        if 'field' in field_file:
            field_data = data_one_field(experiment_dir + field_file)
            field_data_dict = field_data[0]
            field_file_name = field_data[1]
            field_max_ratio = max(i for v in field_data_dict.values() for i in v)
            if field_max_ratio > max_ratio: max_ratio = field_max_ratio
            #print(max_ratio)
    for field_file in os.listdir(experiment_dir):
        if 'field' in field_file:
            field_data = data_one_field(experiment_dir + field_file)
            field_data_dict = field_data[0]
            field_file_name = field_data[1]
            field_ordered_list_data = dict_to_ordered_list(field_data_dict)
            plot_one_field(field_ordered_list_data, plot_dir, field_file_name, max_ratio)

def data_one_field(field_file):
    """
    creates a dictionary of config data for one field file

    INPUT
        one field file (path to field file)

    OUTPUT
        dictionary of ratio data.
        each config file is a key and the value for a config file is a list of ratios.
    """
    f = open(field_file, 'r')
    field_config_data = dict()

    for line in f:
        A = line.split()
        config = A[0]
        data = float(A[1])
        try:
            field_config_data[config].append(data)
        except KeyError:
            field_config_data[config] = [data]
    #print(field_config_data)
    return field_config_data, field_file.split('/')[-1]


def dict_to_ordered_list(field_data_dict):
    """
    converts a dictionary of ratio data for each config to an ordered list.

    INPUT
        dictionary of ratio data.

    OUTPUT
        ordered list of list of ratio.
        order is dictated by the order of configumns (numerical order)
    """
    ordered_list = []
    sorted_keys = list(field_data_dict.keys())
    sorted_keys.sort()
    for x in sorted_keys:
        ordered_list.append(field_data_dict[x])
    return ordered_list


def plot_one_field(field_ordered_list, plot_dir, field_file_name, max_ratio):
    """
    plots boxplots (1 per configumn) of all ratio data)


    """
    plt.figure(figsize=(10, 10))
    plt.boxplot(field_ordered_list)
    plt.xlabel('Configuration')
    plt.xticks(ticks=np.arange(1, 7, 1).tolist(),
                labels=['bz2','fastpfor','fpzip','gzip','zfpy','zlib'],
                rotation=70,
                fontsize=14)
    plt.xlim([0, 6])
    
    plt.ylabel('Compression Ratio ()')
    plt.ylim([0,max_ratio])
    plot_name = field_file_name.split('.')[0]
    plt.title('Column Compression Ratios for ' + plot_name)
    plt.savefig(plot_dir+plot_name+'.png')

if __name__ == "__main__":
    main()


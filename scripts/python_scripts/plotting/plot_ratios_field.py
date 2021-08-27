from matplotlib import pyplot as plt
import numpy as np
import sys
import os

def main():
    max_ratio = 0 
    experiment_dir = sys.argv[1]
    plot_dir = sys.argv[2]
    for field_file in os.listdir(experiment_dir):
        field_data = data_one_field(experiment_dir + field_file)
        field_data_dict = field_data[0]
        field_file_name = field_data[1]
        field_max_ratio = max(i for v in field_data_dict.values() for i in v)
        if field_max_ratio > max_ratio: max_ratio = field_max_ratio
    for field_file in os.listdir(experiment_dir):
        field_data = data_one_field(experiment_dir + field_file)
        field_data_dict = field_data[0]
        field_file_name = field_data[1]
        field_ordered_list_data = dict_to_ordered_list(field_data_dict)
        plot_one_field(field_ordered_list_data, plot_dir, field_file_name, max_ratio)

def data_one_field(field_file):
    """
    creates a dictionary of column data for one field file

    INPUT
        one field file (path to field file)

    OUTPUT
        dictionary of time data.
        each column is a key and the value for a column is a list of times.
        time values are converted from datetime objects to total number of seconds.
    """
    cf = open(field_file, 'r')
    field_column_data = dict()

    for line in cf:
        A = line.split()
        col = int(A[0])
        data = float(A[1])
        try:
            field_column_data[col].append(data)
        except KeyError:
            field_column_data[col] = [data]
    return field_column_data, field_file.split('/')[-1]


def dict_to_ordered_list(field_data_dict):
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
    for x in range(len(field_data_dict)):
        ordered_list.append(field_data_dict[x])
    return ordered_list


def plot_one_field(field_ordered_list, plot_dir, field_file_name, max_ratio):
    """
    plots boxplots (1 per column) of all time data)


    """
    plt.figure(figsize=(10, 10))
    plt.boxplot(field_ordered_list)
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
    plot_name = field_file_name.split('.')[0]
    plt.title('Column Compression Ratios for ' + plot_name)
    plt.savefig(plot_dir+plot_name+'.png')

if __name__ == "__main__":
    main()

#
# def experiment(experiment_dir):
#     """
#     uses read_ratios_data() method on each file in an experiment directory to make dictionaries out of all ratio data
#     INPUT: experiments directory
#     OUTPUT: list of dictionaries
#     """
#     all_dicts = []
#     for ratio_file in os.listdir(experiment_dir):
#         current_dict = read_ratio_data(experiment_dir+ratio_file)
#         all_dicts.append(current_dict)
#     return all_dicts
#
# def read_ratio_data(data_file):
#     ratio_data_dict = dict()
#     f = open(data_file, 'r')
#     for line in f:
#         A = line.split()
#         col_number = int(A[0])
#         ratio_data = float(A[1])
#         try: ratio_data_dict[col_number].append(ratio_data)
#         except KeyError: ratio_data_dict[col_number] = [ratio_data]
#
#     return ratio_data_dict
#
# def plot_all_boxplot(ratio_data_dict, png_file_name):
#     gap = 10
#
#
#     plt.figure(figsize=(50, 50))
#     pos = list(range(0,gap * 10, gap))
#     colors = ['lightcoral', 'lightblue', 'lightgreen',
#               'lightcoral', 'lightblue', 'lightgreen',
#               'lightcoral', 'lightblue', 'lightgreen', 'lightcoral']
#
#     for i in range(len(ratio_data_dict)):
#         curr_experiment = ratio_data_dict[i]
#         curr_p = [p+i for p in pos]
#         # col, positions = p,
#         # labels = ['', '', ''],
#         # # labels=['string', 'int', 'comp'],
#         # notch = None, vert = None,
#         # patch_artist = True,
#         # widths = 1)
#         plt.boxplot([d for d in curr_experiment.values()],
#                     positions=curr_p,
#                     labels=['1','2','3','4','5','6','7','8','9','10'])
#
#         # # fill with colors
#         # colors = ['lightcoral', 'lightblue', 'lightgreen',
#         #           'lightcoral', 'lightblue', 'lightgreen',
#         #           'lightcoral', 'lightblue', 'lightgreen', 'lightcoral']
#         # for patch, color in zip(x['boxes'], colors):
#         #     patch.set_facecolor(color)
#         #
#         # plt.xticks(ticks=np.arange(2, 100, gap).tolist(),
#         #            labels=['col1', 'col2', 'col3', 'col4',
#         #                    'col5', 'col6', 'col7', 'col8',
#         #                    'col9', 'col10'], fontsize=38)
#         # plt.yticks(fontsize=38)
#         # plt.title('Bytes of each column at different points in compression (string, int, compressed)', fontsize=58)
#         # plt.legend(['string data', 'int data', 'compressed data'], fontsize=38,
#         #            labelcolor=colors)
#
#     # plt.boxplot(data1, positions = [1, 2, 3], notch=None, vert=None, patch_artist=None, widths=None)
#     # plt.boxplot(data2, positions = [5, 6, 7], notch=None, vert=None, patch_artist=None, widths=None)
#     # plt.boxplot(data3, positions = [9, 10, 11], notch=None, vert=None, patch_artist=None, widths=None)
#     plt.savefig(png_file_name)
#
# def plot_boxplot(ratio_data_dict, png_file_name):#, num_columns):
#     # plt.boxplot([[1,2,3,4],[10,11,12,13,14],[21,22,23,24]])
#     plt.figure(figsize=(50, 20))
#     plt.boxplot([d for d in ratio_data_dict.values()])
#     plt.xticks(ticks=np.arange(0, 10, 1).tolist(),
#                labels=['col1', 'col2', 'col3', 'col4',
#                        'col5', 'col6', 'col7', 'col8',
#                        'col9', 'col10'], fontsize=38)
#     plt.yticks(fontsize=38)
#     plt.title('title', fontsize=58)
#     plt.savefig(png_file_name)


#x = read_ratio_data("/Users/kristen/PycharmProjects/gwas-compress/plot_data/fastpfor.ratios")
#plot_boxplot(x)#, 10)

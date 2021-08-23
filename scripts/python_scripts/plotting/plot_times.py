from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import sys
import os

def main():
    plt.boxplot([[0.001331, 0.001179, 0.001177], [0.001391, 0.001351, 0.001367], [0.003047, 0.002983, 0.002842],
     [0.002781, 0.002768, 0.002766], [0.002508, 0.002283, 0.002385], [0.002267, 0.002073, 0.002136],
     [0.002316, 0.002125, 0.00215], [0.002255, 0.002063, 0.002119], [0.002245, 0.002043, 0.002075],
     [0.008564, 0.008192, 0.008567]])
    plt.title('testing')
    plt.savefig('/Users/kristen/PycharmProjects/gwas-compress/plots/testing.png')

    experiment_dir = sys.argv[1]
    for config_file in os.listdir(experiment_dir):
        config_data = data_one_config(experiment_dir + config_file)
        config_data_dict = config_data[0]
        config_file_name = config_data[1]
        config_ordered_list_data = dict_to_ordered_list(config_data_dict)
        plot_one_config(config_ordered_list_data, config_file_name)

    # png_file_name = sys.argv[2]
    # print(png_file_name)
    # all_dicts = experiment(experiment_dir)
    # plot_all_boxplot(all_dicts, png_file_name)
    # print(len(all_dicts))

def data_one_config(config_file):
    cf = open(config_file, 'r')
    config_column_data = dict()
    print(config_file)

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

def plot_one_config(config_ordered_list, config_file_name):
    plt.figure(figsize=(10,10))
    plt.ylim([0,0.02])
    plt.xlim([0,10])
    plt.boxplot(config_ordered_list)
    plot_name = config_file_name.split('.')[0]
    plt.title(plot_name)
    plt.savefig('/Users/kristen/PycharmProjects/gwas-compress/plots/'+plot_name+'.png')

#
# def experiment(experiment_dir):
#     """
#     uses read_times_data() method on each file in an experiment directory to make dictionaries out of all time data
#     INPUT: experiments directory
#     OUTPUT: list of dictionaries
#     """
#     all_dicts = []
#     for time_file in os.listdir(experiment_dir):
#         current_dict = read_time_data(experiment_dir+time_file)
#         all_dicts.append(current_dict)
#     return all_dicts
#
# def read_time_data(data_file):
#     time_data_dict = dict()
#     f = open(data_file, 'r')
#     for line in f:
#         A = line.split()
#         col_number = int(A[0])
#         time_data = datetime.strptime(A[1], '%H:%M:%S.%f')
#         seconds = time_data.second
#         microseconds = time_data.microsecond
#         total_seconds = (seconds + microseconds/1e6)
#         try:
#             time_data_dict[col_number].append(total_seconds)
#         except KeyError: time_data_dict[col_number] = [total_seconds]
#     return time_data_dict
#
# def plot_all_boxplot(time_data_dict, png_file_name):
#     gap = 6
#
#     plt.figure(figsize=(50, 20))
#     pos = list(range(0, 6 * 10, 6))
#     colors = ['lightcoral', 'black', 'white',
#             'lightcoral', 'peru', 'gold']
#             # 'olivedrab', 'steelblue', 'mediumpurple',
#             # 'palevioletred', 'black', 'silver', 'white']
#
#     for i in range(len(time_data_dict)):
#         curr_experiment = time_data_dict[i]
#         curr_p = [p+i for p in pos]
#         # col, positions = p,
#         # labels = ['', '', ''],
#         # # labels=['string', 'int', 'comp'],
#         # notch = None, vert = None,
#         # patch_artist = True,
#         # widths = 10
#         # x = plt.boxplot([d for d in curr_experiment.values()],
#         #             positions=curr_p,
#         #             notch = None, vert = None, patch_artist = True)
#         #             #labels=)
#
#         # for patch, color in zip(x['boxes'], colors):
#         #     patch.set_facecolor(color)
#
#         plt.xticks(ticks=np.arange(3, gap * 10, gap).tolist(),
#                    labels=['col1', 'col2', 'col3', 'col4',
#                            'col5', 'col6', 'col7', 'col8',
#                            'col9', 'col10'], fontsize=38)
#         plt.yticks(fontsize=38)
#         # plt.title('Bytes of each column at different points in compression (string, int, compressed)', fontsize=58)
#         # plt.legend(['string data', 'int data', 'compressed data'], fontsize=38,
#         #            labelcolor=colors)
#     pos = list(range(0, len(time_data_dict[0][0])))
#
#     print(len(time_data_dict))
#     for x in range(len(time_data_dict)):
#         # print(time_data_dict[x].values())
#         y = plt.boxplot([d for d in time_data_dict[x].values()], patch_artist=True)
#
#
#     # plt.boxplot(time_data_dict[0], positions=pos)#, notch=None, vert=None, patch_artist=None, widths=None)
#     # plt.boxplot(data2, positions = [5, 6, 7], notch=None, vert=None, patch_artist=None, widths=None)
#     # plt.boxplot(data3, positions = [9, 10, 11], notch=None, vert=None, patch_artist=None, widths=None)
#     plt.savefig(png_file_name)


if __name__ == "__main__":
    main()

# def plot_boxplot(time_data_dict, png_file_name):#, num_columns):
#     # plt.boxplot([[1,2,3,4],[10,11,12,13,14],[21,22,23,24]])
#     plt.figure(figsize=(50, 20))
#     plt.boxplot([d for d in time_data_dict.values()])
#     plt.xticks(ticks=np.arange(0, 10, 1).tolist(),
#                labels=['col1', 'col2', 'col3', 'col4',
#                        'col5', 'col6', 'col7', 'col8',
#                        'col9', 'col10'], fontsize=38)
#     plt.yticks(fontsize=38)
#     plt.title('title', fontsize=58)
#     plt.savefig(png_file_name)

#x = read_time_data("/Users/kristen/PycharmProjects/gwas-compress/plot_data/fastpfor.times")
#plot_boxplot(x)#, 10)

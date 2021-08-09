from matplotlib import pyplot as plt
import numpy as np
import sys
import os

def main():
    experiment_dir = sys.argv[1]
    #ratio_data_file = sys.argv[1]
    png_file_name = sys.argv[2]
    all_dicts = experiment(experiment_dir)
    print(len(all_dicts))
    #ratio_data_dict = read_ratio_data(ratio_data_file)
    #plot_boxplot(ratio_data_dict, png_file_name)

def experiment(experiment_dir):
    """
    uses read_ratios_data() method on each file in an experiment directory to make dictionaries out of all ratio data
    INPUT: experiments directory
    OUTPUT: list of dictionaries
    """
    all_dicts = []
    for ratio_file in os.listdir(experiment_dir):
        current_dict = read_ratio_data(experiment_dir+ratio_file)
        all_dicts.append(current_dict)
    return all_dicts

def read_ratio_data(data_file):
    ratio_data_dict = dict()
    f = open(data_file, 'r')
    for line in f:
        A = line.split()
        col_number = int(A[0])
        ratio_data = float(A[1])
        try: ratio_data_dict[col_number].append(ratio_data)
        except KeyError: ratio_data_dict[col_number] = [ratio_data]

    return ratio_data_dict

def plot_all_boxplot(ratio_data_dict):

def plot_boxplot(ratio_data_dict, png_file_name):#, num_columns):
    # plt.boxplot([[1,2,3,4],[10,11,12,13,14],[21,22,23,24]])
    plt.figure(figsize=(50, 20))
    plt.boxplot([d for d in ratio_data_dict.values()])
    plt.xticks(ticks=np.arange(0, 10, 1).tolist(),
               labels=['col1', 'col2', 'col3', 'col4',
                       'col5', 'col6', 'col7', 'col8',
                       'col9', 'col10'], fontsize=38)
    plt.yticks(fontsize=38)
    plt.title('title', fontsize=58)
    plt.savefig(png_file_name)

if __name__ == "__main__":
    main() 

#x = read_ratio_data("/Users/kristen/PycharmProjects/gwas-compress/plot_data/fastpfor.ratios")
#plot_boxplot(x)#, 10)

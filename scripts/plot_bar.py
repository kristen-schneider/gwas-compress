# import ../block_pyfast
import matplotlib.pyplot as plt
import os
import datetime
import statistics
import numpy as np



def main():
    print(get_dict_data())
    #data = get_data(i_file)
    #plot_data(data)

def get_data(i_file):
    x = []
    y = []

    f = open(i_file, 'r')
    for line in f:
        A = line.rstrip().split()
        x.append(A[0])
        y.append(float(A[1]))

    return x, y        

def get_dict_data(out_dir):
    """

    """
    # format [column: compression_method[block1time, block2time...]]
    dict_data = {}

    for col_comp_file in os.listdir(out_dir):
        if 'column' in col_comp_file:
            f = open(out_dir+col_comp_file)
            all_data_str = f.readline().split(',')[0:-2]
            all_data_time = time_to_float(all_data_str)

            full_name = col_comp_file.split('.')[0].split('_')
            column_number = int(full_name[0].replace('column', ''))
            compression_method = full_name[1]

            try: dict_data[column_number][compression_method] = statistics.mean(all_data_time)
            except KeyError: dict_data[column_number] = {compression_method: statistics.mean(all_data_time)}

            # try: dict_data[column_number][compression_method].append()


            print(col_comp_file)

    return dict_data

def time_to_float(all_data_str):
    all_data_time = []
    for d in all_data_str:
        full_seconds = 0
        time = datetime.datetime.strptime(d, '%H:%M:%S.%f')

        time_zero = datetime.datetime.strptime('0:00:00.000000', '%H:%M:%S.%f')
        time_delta = time - time_zero
        total_seconds = time_delta.total_seconds()
        all_data_time.append(total_seconds)
    return all_data_time

def plot_data(dict_data, available_compression_methods):
    # x = data[0]
    # y = data[1]
    # print(x)
    # print(y)
    #y = [1, 2, 4, 5, 6, 8, 2, 3, 4, 5, 6, 7, 8, 9, 11, 1, 3, 5, 2, 3, 8, 3, 13, 3, 4, 8, 2, 4, 9, 7, 8, 3, 11]
    #x = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'sept', 'oct', 'nov', 'dec']
    #y = [31, 28, 100, 40, 65, 82, 12, 90, 34, 43, 87, 20]
    column_labels = [c for c in sorted(dict_data.keys())]

    for col in dict_data:
        for method in dict_data[col]:
            plt.bar(column_labels-0.2, data, 0.4)
            data = dict_data[col].values()
            q = dict_data[col][method]
            plt.bar()


    pos = np.arange(len(column_labels))

    plt.figure(figsize=(15,20))
    plt.bar(x, y, bottom=0)
    plt.xticks(pos, x, rotation=70)
    plt.xlabel('codec')
    plt.ylabel('compression ratio')
    plt.savefig('/home/krsc0813/projects/gwas-compress/plot_data/codecs_plot.png')

if __name__ == '__main__':
    main()

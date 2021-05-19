# import ../block_pyfast
import matplotlib.pyplot as plt
import numpy as np
import read_write_compression_times
import statistics


def main():
    print(get_dict_data())



def plot_data(dict_data, available_compression_methods):
    x = data[0]
    y = data[1]
    print(x)
    print(y)
    y = [1, 2, 4, 5, 6, 8, 2, 3, 4, 5, 6, 7, 8, 9, 11, 1, 3, 5, 2, 3, 8, 3, 13, 3, 4, 8, 2, 4, 9, 7, 8, 3, 11]
    x = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'sept', 'oct', 'nov', 'dec']
    y = [31, 28, 100, 40, 65, 82, 12, 90, 34, 43, 87, 20]
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






def plot_loop(data):
    #
    plt.bar(data)

def get_loop_dict(out_dir, num_columns, available_compression_methods):
    # data for plotting
    # {method1: {col1: data}, {col2: data}, {col3: data}...}

    # create empty dict data
    full_data_dict = {}
    for method in range(len(available_compression_methods)):
        full_data_dict[method] = {}
    for col_key in full_data_dict:
        for method in available_compression_methods:
            full_data_dict[col_key][method] = []

    for col in range(num_columns):
        for comp_method in available_compression_methods:
            f = out_dir + 'column' + str(col) + '_' + comp_method + '.csv'
            print(f)
            try: data_all_blocks = read_write_compression_times.read_times(f)
            except FileNotFoundError: continue
            avg_time = statistics.mean(data_all_blocks)
            # try:
            #     f = out_dir+'column'+str(col)+'_'+comp_method+'.csv'
            #     data = f.readline().split(',')[0:-1]
            #     print(f, data)
            #
            # except FileNotFoundError: continue

def get_loop_data(dict):





if __name__ == '__main__':
    main()

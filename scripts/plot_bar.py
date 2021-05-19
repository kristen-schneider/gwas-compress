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


def plot_loop(data, num_cols, available_compression_methods):
    num_methods = len(data)
    col_labels = [(('column'+str(i+1))) for i in range(num_cols)]
    x_axis_anchor = np.arange(num_methods)
    max_val = 1
    increment = num_methods
    x_axis_delta = np.linspace(-max_val, max_val, num=increment)

    plt.figure(figsize=(15,20))

    for cm in range(len(available_compression_methods)):
        current_pos_delta = x_axis_delta[cm]
        current_comp_method = available_compression_methods[cm]
        current_data = data[current_comp_method]
        width = 10/num_methods
        plt.bar(x_axis_anchor+current_pos_delta, current_data, width, label=col_labels[cm])

    # for m in range(num_methods):


def get_loop_dict(out_dir, num_columns, available_compression_methods):
    # data for plotting
    # {method1: {col1: data}, {col2: data}, {col3: data}...}

    # create empty dict data
    full_data_dict = {}
    for method in available_compression_methods:
        full_data_dict[method] = {}
    for method_key in full_data_dict:
        for col in range(num_columns):
            full_data_dict[method_key][col] = get_col_method_avg(out_dir, col, method_key)

    return full_data_dict

def get_col_method_avg(out_dir, col, method):
    try:
        f = out_dir + 'column' + str(col) + '_' + method + '.csv'
        data_all_blocks = read_write_compression_times.read_times(f)
        avg_time = statistics.mean(data_all_blocks)
    except FileNotFoundError:
        avg_time = None
    return avg_time

def get_final_data(full_data_dict, available_compression_methods, num_cols):
    # {method1: [col1, col2, col3...], method2: [col1, col2, col3...]}
    final_data= {}
    for cm in available_compression_methods:
        for col in range(num_cols):
            try: final_data[cm].append(full_data_dict[cm][col])
            except KeyError: final_data[cm] = [full_data_dict[cm][col]]

    return final_data

# def mirrored(max_val, increment):
#     x = np.arange(increment, max_val, increment)
#     if x[-1] != max_val:
#         x = np.r_[x, max_val]
#     return np.r_[-x[::-1], 0, x]

if __name__ == '__main__':
    main()

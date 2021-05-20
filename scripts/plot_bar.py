# import ../block_pyfast
import matplotlib.pyplot as plt
import numpy as np
import read_write_compression_times
import read_write_compression_ratios
import statistics

def plot_loop_times(data, num_cols, available_compression_methods):
    num_methods = len(data)

    x_labels = [(('column'+str(i+1))) for i in range(num_cols)]
    x_axis_anchor = np.arange(num_cols)*2
    max_val = 1
    increment = num_methods+1
    x_axis_delta = np.linspace(-max_val, max_val, num=increment)

    plt.figure(figsize=(15,20))

    for cm in range(len(available_compression_methods)):
        current_pos_delta = x_axis_delta[cm]
        current_comp_method = available_compression_methods[cm]
        current_data = data[current_comp_method]
        #print(current_data)
        width = 2/num_methods
        plt.bar(x_axis_anchor+current_pos_delta, current_data, width,
                label=available_compression_methods[cm])

    plt.xticks(x_axis_anchor, x_labels, rotation=70)
    plt.xlabel('column')
    plt.ylabel('compression time (seconds)')
    plt.title('compression time for ' + str(len(available_compression_methods)) + ' different compression methods')
    plt.legend(prop={'size': 30})
    plt.savefig('times.png')
    # for m in range(num_methods):

def plot_loop_ratios(data, num_cols, available_compression_methods):
    num_methods = len(data)

    x_labels = [(('column'+str(i+1))) for i in range(num_cols)]
    x_axis_anchor = np.arange(num_cols)*2
    max_val = 1
    increment = num_methods+1
    x_axis_delta = np.linspace(-max_val, max_val, num=increment)

    plt.figure(figsize=(15,20))

    for cm in range(len(available_compression_methods)):
        current_pos_delta = x_axis_delta[cm]
        current_comp_method = available_compression_methods[cm]
        current_data = data[current_comp_method]
        #print(current_data)
        width = 2/num_methods
        plt.bar(x_axis_anchor+current_pos_delta, current_data, width,
                label=available_compression_methods[cm])

    plt.xticks(x_axis_anchor, x_labels, rotation=70)
    plt.xlabel('column')
    plt.ylabel('compression ratios (before/after in bytes)')
    plt.title('compression time for ' + str(len(available_compression_methods)) + ' different compression methods')
    plt.legend(prop={'size': 30})
    plt.savefig('ratios.png')
    # for m in range(num_methods):

def get_loop_dict(out_dir, num_columns, available_compression_methods, measurement):
    # data for plotting
    # {method1: {col1: data}, {col2: data}, {col3: data}...}

    # create empty dict data
    full_data_dict = {}
    for method in available_compression_methods:
        full_data_dict[method] = {}
    for method_key in full_data_dict:
        for col in range(num_columns):
            full_data_dict[method_key][col] = get_col_method_avg(out_dir, col, method_key, measurement)

    return full_data_dict

def get_col_method_avg(out_dir, col, method, measurement):
    try:
        f = out_dir + 'column' + str(col) + '_' + method + '.csv'
        if measurement == 'times': data_all_blocks = read_write_compression_times.read_times(f)
        elif measurement == 'ratios': data_all_blocks = read_write_compression_ratios.read_ratios(f)
        avg_time = statistics.mean(data_all_blocks)
    except FileNotFoundError:
        avg_time = 0
    return avg_time

def get_final_data(full_data_dict, available_compression_methods, num_cols):
    # {method1: [col1, col2, col3...], method2: [col1, col2, col3...]}
    final_data= {}
    for cm in available_compression_methods:
        for col in range(num_cols):
            try: final_data[cm].append(full_data_dict[cm][col])
            except KeyError: final_data[cm] = [full_data_dict[cm][col]]

    return final_data

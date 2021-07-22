def write_ratios(all_column_compression_size_ratios, out_dir):
    for col in all_column_compression_size_ratios:
        for comp_method in all_column_compression_size_ratios[col]:
            df = open(out_dir + 'column' + str(col) + '_' + comp_method + '.csv', 'w')
            for d in range(len(all_column_compression_size_ratios[col][comp_method])):
                # print(type(all_column_compression_times[col][comp_method][d]))
                ratio = all_column_compression_size_ratios[col][comp_method][d]
                df.write(str(ratio) + ',')


def read_ratios(f):
    f_open = open(f, 'r')
    str_data_list = f_open.readline().split(',')[0:-1]
    float_data_list = [float(d) for d in str_data_list]
    return float_data_list

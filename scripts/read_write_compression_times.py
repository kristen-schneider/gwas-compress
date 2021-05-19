import datetime


def write_times(all_column_compression_times, out_dir):
    for col in all_column_compression_times:
        for comp_method in all_column_compression_times[col]:
            df = open(out_dir + 'column' + str(col) + '_' + comp_method + '.csv', 'w')
            for d in range(len(all_column_compression_times[col][comp_method])):
                # print(type(all_column_compression_times[col][comp_method][d]))
                time = all_column_compression_times[col][comp_method][d]
                df.write(str(all_column_compression_times[col][comp_method][d]) + ',')


def read_times(f):
    f_open = open(f, 'r')
    str_data_list = f_open.readline().split(',')[0:-1]
    float_data_list = time_to_float(str_data_list)
    return float_data_list


def time_to_float(str_data_list):
    all_data_time = []
    for d in str_data_list:
        time = datetime.datetime.strptime(d, '%H:%M:%S.%f')
        time_zero = datetime.datetime.strptime('0:00:00.000000', '%H:%M:%S.%f')
        time_delta = time - time_zero

        total_seconds = time_delta.total_seconds()
        all_data_time.append(total_seconds)

    return all_data_time

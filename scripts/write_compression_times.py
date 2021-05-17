
def write_times(all_column_compression_times, compression_times_file):
    num_blocks = len(all_column_compression_times[0])

    header = []
    for i in range(num_blocks): header.append('block'+str(i+1))


    ct_f = open(compression_times_file, 'w')
    ct_f.write('column')
    for h in header: ct_f.write(','+h)
    ct_f.write('\n')

    for column_i in range(len(all_column_compression_times)):
        column = all_column_compression_times[column_i]
        ct_f.write(str(column_i+1))
        for time in column:
            ct_f.write(','+str(time))
        ct_f.write('\n')
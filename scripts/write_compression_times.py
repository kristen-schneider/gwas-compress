
def write_times(all_column_compression_times, out_dir):

    for col in all_column_compression_times:
        for comp_method in all_column_compression_times[col]:
            df = open(out_dir+'column' + str(col)+'_'+comp_method+'.csv', 'w')
            for d in range(len(all_column_compression_times[col][comp_method])):
                df.write(str(all_column_compression_times[col][comp_method][d])+',')

    # for column_i in range(len(all_column_compression_times)):
    #     column = all_column_compression_times[column_i]
    #     ct_f.write(str(column_i+1))
    #     for time in column:
    #         ct_f.write(','+str(time))
    #     ct_f.write('\n')
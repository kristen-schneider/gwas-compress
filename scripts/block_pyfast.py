import pyfastpfor_test
import generate_funnel_format
import type_handling

# in data:
#[['1', '1', '1'], ['11063', '13259', '17641'], ['T', 'G', 'G'], ['G', 'A', 'A'], ['4.213e-05', '2.984e-05', '7.127e-04'], ['4.799e-05', '2.786e-04', '8.313e-04'], ['-1.334e+00', '-1.047e+00', '-9.812e-02'], ['9.999e+00', '1.448e+00', '8.260e-01'], ['8.938e-01', '4.699e-01', '9.054e-01'], ['true', 'true', 'true']]
#[['1', '1', '1'], ['30741', '51427', '57222'], ['C', 'T', 'T'], ['A', 'G', 'C'], ['NA', 'NA', '8.637e-04'], ['NA', 'NA', '6.581e-04'], ['NA', 'NA', '6.134e-01'], ['NA', 'NA', '9.714e-01'], ['NA', 'NA', '5.277e-01'], ['NA', 'NA', 'true']]
#[['1', '1', '1'], ['58396', '62745', '63668'], ['T', 'C', 'G'], ['C', 'G', 'A'], ['0.000e+00', 'NA', '0.000e+00'], ['2.409e-04', 'NA', '2.780e-05'], ['-1.007e+00', 'NA', '-1.287e+00'], ['1.437e+00', 'NA', '4.597e+00'], ['4.833e-01', 'NA', '7.795e-01'], ['true', 'NA', 'true']]


IN_FILE = '/home/krsc0813/projects/gwas-compress/data/hundred_thousand.tsv'
OUT_FILE = '/home/krsc0813/projects/gwas-compress/plot_data/'
BLOCK_SIZE = 20000
NUM_COLS = 10
DELIMITER = '\t'
COL_TYPES = [1, 1, 3, 3, 2, 2, 2, 2, 2, 3]

def main():
    ff = generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLS, DELIMITER)
    for block_i in range(len(ff)):
        curr_block = ff[block_i]
        for column_i in range(len(curr_block)):
            curr_column = curr_block[column_i]
            column_type = COL_TYPES[column_i]
            typed_column = type_handling.convert_to_type(curr_column, column_type)


            if column_type == 1:
                #print(column_i, typed_column)
            
                pyfastpfor_test.kristen(column_i, typed_column, OUT_FILE)
    #arr = [1] * 200
    #pyfastpfor_test.kristen(arr)
    
if __name__ == '__main__':
    main()
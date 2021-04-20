import pyfastpfor_test
import /scratch/Users/krsc0813/gwas-compress/scripts/generate_funnel_format

IN_FILE = '/scratch/Users/krsc0813/gwas-compress/data/test-gwas-data/test.tsv'
BLOCK_SIZE = 3
NUM_COLS = 10
DELIMITER = '\t'

def main():
    generate_funnel_format.make_all_blocks(IN_FILE, BLOCK_SIZE, NUM_COLS, DELIMITER)
    #arr = [1] * 200
    #pyfastpfor_test.kristen(arr)
    
if __name__ == '__main__':
    main()

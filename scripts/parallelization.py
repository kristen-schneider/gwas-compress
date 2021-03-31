import multiprocessing
from multiprocessing.pool import Pool

#EXAMPLE
def main():
    arr_inputs=[1,2,3]

    with Pool(3) as p:
        arr_outputs = p.map(add_to_five, arr_inputs)

    print(arr_outputs)

def compress_in_parallel(block):
    compressed_block = b''
    return compressed_block

def add_to_five(x):
      return x+5

if __name__ == '__main__':
    main()




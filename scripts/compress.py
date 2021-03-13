import gzip
import serialize

def main():
    bitstring = serialize.serialize_data()
    compressed_data = compress_data(bitstring)    

def compress_data(bitstring):
    return gzip.compress(bitstring)

if __name__ == '__main__': main()

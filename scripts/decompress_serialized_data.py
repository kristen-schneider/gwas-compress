import deserialize
import decompress

def decompress_single_column(compression_method, c_bitstring, block_size, data_type, num_bytes, chrm):
    print('decompressing with regular serialization')
    """
    decompresses a single column of data using gzip/zlib/bz2
    
    INPUT
        compressed_arr = numpy array of compressed data
        arr_size = size to allocate for decompressed data
        codec = compression method

    OUTPUT
        decompressed_column = decompressed data (np array)
    """
    dc_column = decompress.decompress_data(compression_method, c_bitstring)
    ds_column = deserialize.deserialize_data(dc_column, block_size, data_type, num_bytes, chrm)
    return ds_column

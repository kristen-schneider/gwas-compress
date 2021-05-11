import serialize
import compress

def compress_single_column(typed_column, column_compression_method, column_type, column_bytes, mtime):
    """
    compresses a single column of data using methods that take in serialized data (e.g. gzip, zlib, bz2)

    INPUT
        typed_column = column as proper type (list of ints, rather than strings)
        column_compression_method = method of compression for given column
        column_type = data type for given column
        column_bytes = number of bytes used for compression
        mtime = for gzip.compress input

    OUTPUT
        compressed_column_info = compressed data and length of header which would help decompress data
    """
    serialized_column = serialize.serialize_list(typed_column, column_type, column_bytes)
    compressed_column_info = compress.compress_data(column_compression_method, serialized_column, mtime)
    return compressed_column_info

# import packed_strings
# import hybrid_strings
# import convert_to_int
from datetime import datetime


#import ref_alt_smaller_ints

def get_column_types(row):
    """
    Given a row of data, returns all the types of data in that row
    Data types are according to code_book

    INPUT
        row = list of data that we see in a row (e.g. ['1', 'A', ...]

    OUTPUT
        data_types_list = list of data types witnessed in that row (e.g. [1, 2, 2, 1, 1...])
    """
    data_types_list = []
    for r in row:
        data_type = get_data_type(r)
        data_types_list.append(data_type)
    return data_types_list


def get_data_type(str_data):
    """
    Returns proper data type of incoming data. This is used only once for a the first row.
    Most data is read in as a string. this will try and discern if it is actually an integer/float.
    We use a dictionary/code book to label each type because we cannot pass types as parameters.

    INPUT
        data = incoming data. likely to be read in as string
    OUTPUT
        data_type = int, float, or str
    """

    # hierarchy: int, float, string
    try:
        int(str_data)
        # all integers are of type 1.
        # chromosomes which are non numeric need further breakdown in conversion step
        return 1
    except ValueError:
        try:
            float(str_data)
            # all floats are of type 2
            return 2
        except ValueError:
            try:
                str(str_data)
                # string data for true / false values are of type 3
                if 'false' in str_data.lower() or 'true' in str_data.lower() or 'na' in str_data.lower():
                    return 3
                # string data for SNP and INDELs are of type 4
                else:
                    return 4
            except ValueError:
                print('could not detect data type as int, float, or string')
                return type(str_data)

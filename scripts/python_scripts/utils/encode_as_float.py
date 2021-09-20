def encode_column_as_float(column, column_data_type):
    """
    converts a whole column to data type float.
    """
    column_as_float = []

    # for all others we encode each data point individually as int
    for data in column:
        float_data = convert_data_type_to_float(data, column_data_type)
        column_as_float.append(float_data)
    return column_as_float

def convert_data_type_to_float(data, column_data_type):
    if column_data_type == 1:
        try: return float(data)
        except ValueError:
            if data.lower() == 'x': return(float(23))
            elif data.lower() == 'y': return(float(24))
    
    elif column_data_type == 2:
        try: return(float(data))
        except ValueError:
            # NA values return value not seen in data (99)
            if data.lower() == 'na':
                return float('nan')
    #else:
    #    try:
    #        if data.lower() == 'x': return(float(23))
    #        elif data.lower() == 'y': return(float(24))
    #    except ValueError:
    #        print('cannot convert ', data, ' to float')
    #    return None

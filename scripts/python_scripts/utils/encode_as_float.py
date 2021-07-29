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
        return float(data)
    elif column_data_type == 2:
        try: return float(data)
        except ValueError:
            # NA values return value not seen in data (999)
            if data.lower() == 'NA':
                return float(999)
    else:
        print('cannot convert ', data, ' to float')
        return None

def convert_any_data_to_int(data, data_type):
    """
    given any data in string format ('int', 'float', 'string', 'bytes'), converts to integer
    INPUT
        data = itput data
        data_type = original data type

    OUTPUT
        integer version of data
    """
    if data_type == 1:
        return int_to_int(data)
    elif data_type == 2:
        return float_to_int(data)
    elif data_type == 3:
        #return data
        return string_to_int(data)
    elif data_type == 4:
        return bytes_to_int(data)

def int_to_int(in_data):
    """
    converts string 'int' to type int

    INPUT
        in_data: input data (string representation of integer data)

    OUTPUT
        out_data: integer value representing in_data (X = 23, Y = 24)
    """
    int_data = None
    try:
        return int(in_data)
    except ValueError:
        if in_data == 'X':
            int_data = 23
        elif in_data == 'Y':
            int_data = 24
        else: print('cannot convert data to int')
    return int_data

def float_to_int(float_data):
    """
    converts a data type of float to a list of integers which can reconstruct the float

    INPUT
        float_data: data in float form (e.g. 4.213e-05)

    OUTPUT
        int_data: large integer with little endian formatting number:
        base  exp -/+
        00000 000 0
    """
    # 000000000 - little endian
    float_as_int = 0
    if float_data == 'NA':
        # choose a value that is not seen in data
        float_as_int = 999
    else:
        # base, base_sign, exponent, exponent_sign
        # 00000, 0, 00, 0,

        base_exponent = float_data.split('e')
        base = float(base_exponent[0])
        exponent = int(base_exponent[1])

        # BASE
        # base number gets proper space (e.g. 4.213 --> 42130)
        # have to do this in two steps because
        # rounding is lossy with python_scripts multiplication
        # if we just did *100000000 we would get junk in the last 4 digits
        float_as_int += abs(int(base*10000))
        float_as_int *= 10000

        # BASE SIGN
        # is number negative or positive?
        base_sign = 1  # positive
        if float(base) < 0: base_sign = 0  # negative
        float_as_int += base_sign * 1000

        # EXPONENT
        # exponents must be < 100
        # otherwise the placement of the exponent bleeds into the base/base sign
        float_as_int += abs(exponent) * 10

        # EXPONENT SIGN
        if exponent > 0: float_as_int += 1

    return float_as_int


def string_to_int(string_data):
    """
    takes string input and converts to integer.
        false = 0
        true = 1
        #A, C, G, T = 2, 3, 4, 5
        NA = -1

    INPUT
        string_data = single data value of type string

    OUTPUT
        int_data = string data converted to integer value according to mapping above.
    """
    # A,C,T,G = 2,3,4,5
    # -2 flags start of indel

    int_data = []

    if len(string_data) > 1:
        if string_data == 'false':
            int_data = 0
        elif string_data == 'true':
            int_data = 1
        elif string_data == 'NA':
            int_data = 2
        else:
            return string_data
        return int_data
        #else:
            #for s in string_data:
            #    int_data.append(single_string_to_int(s))
    else:
        return string_data
        #int_data = single_string_to_int(string_data)
    return string_data

def single_string_to_int(string_data):
    """
    one single string value

    """
    if string_data == 'A':
        int_data = 2
    elif string_data == 'C':
        int_data = 3
    elif string_data == 'G':
        int_data = 4
    elif string_data == 'T':
        int_data = 5
    else:
        try:
            int_data = int(string_data)
        except ValueError:
            print('cannot convert string to int')
            return int_data
    return int_data



i1 = '3'
i2 = 'X'
f = '1.234e-05'
s1 = 'true'
s2 = 'A'
s3 = 'AAA'

print(int_to_int(i1), int_to_int(i2))
print(float_to_int(f))
print(string_to_int(s1), string_to_int(s2), string_to_int(s3))
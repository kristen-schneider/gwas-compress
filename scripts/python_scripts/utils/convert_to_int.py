from utils import packed_strings
from utils import hybrid_strings
def convert_data_type_to_int(data, data_type):
    """
    given any data in string format ('int', 'float', 'string', 'bytes'), converts to integer
    INPUT
        data = input data, single valu
        data_type = original data type ('1' = int, '1.234e-05' = float, 'true' = string)

    OUTPUT
        integer version of data
    """
    if data_type == 1:
        return int_to_int(data)
    elif data_type == 2:
        return float_to_int(data)
    elif data_type == 3: # true/false strings
        return true_false_to_int(data)
    elif data_type == 4: # SNP/INDEL
        return packed_strings.
    else:
        return None
        # return bytes_to_int(data)

def int_to_int(in_data):
    """
    converts string 'int' to type int

    INPUT
        in_data: input data (string representation of integer data)

    OUTPUT
        ** must make room for non human genomes **
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
    converts a data type of float to an integer which can reconstruct the float

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


def true_false_to_int(tf_data):
    """
    takes string input and converts to integer.
        false = 0
        true = 1
        NA = -1

    INPUT
        string_data = single data value of type string

    OUTPUT
        int_data = string data converted to integer value according to mapping above.
    """
    int_data = None

    if tf_data.tolower() == 'false':
        int_data = 0
    elif tf_data.tolower() == 'true':
        int_data = 1
    elif tf_data.tolower() == 'NA':
        int_data = -1
    else:
        print('cannot covert true/false data to int.')
        return None
    return int_data

i1 = '3'
i2 = 'X'
f = '1.234e-05'
s1 = 'true'
s2 = 'A'
s3 = 'AAA'

print(int_to_int(i1), int_to_int(i2))
print(float_to_int(f))
print(true_false_to_int(s1), true_false_to_int(s2), true_false_to_int(s3))
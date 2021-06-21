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
        # rounding is lossy with python multiplication
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


def int_to_float(int_data):
    """
    converts a data type of int to a float
    (for decompressing float columns)

    INPUT
        int_data: data in int form (e.g. 42130050)

    OUTPUT
        int_as_float: data in float form (e.g. 4.213e-05)
    """
    # base, base_sign, exponent, exponent_sign
    # 00000, 0, 00, 0,

    int_as_float = 0
    if int_data == 999:
        # choose a value that is not seen in data
        int_as_float = 'NA'
    else:
        int_as_float = get_float_parts(int_data)
    return int_as_float

def get_float_parts(int_data):
    base = int(int_data/10000)
    decimal_base = float(base/10000)

    leftover = int(int_data-(base*10000))

    base_sign = int(leftover/1000)
    leftover -= base_sign*1000

    exponent = int(leftover/10)
    leftover -= exponent*10

    exponent_sign = leftover

    int_as_float = construct_float(decimal_base, base_sign, exponent, exponent_sign)

    return int_as_float

def construct_float(base, base_sign, exponent, exponent_sign):
    f = round(base, 4)
    if exponent_sign == 0:
        exponent *= -1

    if base_sign == 0:
        f = -1 * base * pow(10, exponent)
    else:
        f = base * pow(10, exponent)

    return f
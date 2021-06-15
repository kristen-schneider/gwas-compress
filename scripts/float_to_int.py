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


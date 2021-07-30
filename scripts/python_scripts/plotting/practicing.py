def read_ratio_data(data_file):
    ratio_data_dict = dict()
    f = open(data_file, 'r')
    for line in f:
        A = line.split()
        col_number = int(A[0])
        ratio_data = float(A[1])
        try: ratio_data_dict[col_number].append(ratio_data)
        except KeyError: ratio_data_dict[col_number] = [ratio_data]

    return ratio_data_dict

x = read_ratio_data("/Users/kristen/PycharmProjects/gwas-compress/plot_data/fastpfor.ratios")
print(x)
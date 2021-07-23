import matplotlib.pyplot as plt
import numpy as np

def boxplot_read_fastp_file(fastp_file, num_columns):
    f = open(fastp_file, 'r')
    delimiter = '\t'

    strings_data = {col:[] for col in range(10)}
    int_data = {col:[] for col in range(10)}
    comp_data = {col:[] for col in range(10)}

    block = 0
    for line in f:
        curr_block = line.split(delimiter)
        d = 0
        for data in range(num_columns):
            strings_data[data].append(int(curr_block[d]))
            int_data[data].append(int(curr_block[d+1]))
            comp_data[data].append(int(curr_block[d+2]))

            d += 3


        block += 1

    return strings_data, int_data, comp_data


def boxplot_bytes_storage(strings_data, ints_data, compressed_data):
    pos1 = 1
    pos2 = 2
    pos3 = 3
    gap = 10

    cols_data = make_cols_data(strings_data, ints_data, compressed_data)

    plt.figure(figsize=(50, 20))
    for col in cols_data:
        p = [pos1, pos2, pos3]
        x = plt.boxplot(col, positions=p,
                    labels=['','',''],
                    # labels=['string', 'int', 'comp'],
                    notch=None, vert=None,
                    patch_artist=True,
                    widths=1)

        # fill with colors
        colors = ['lightcoral', 'lightblue', 'lightgreen']
        for patch, color in zip(x['boxes'], colors):
            patch.set_facecolor(color)

        plt.xticks(ticks= np.arange(2, 100, gap).tolist(),
                   labels=['col1', 'col2', 'col3', 'col4',
                           'col5', 'col6', 'col7', 'col8',
                           'col9', 'col10'], fontsize=38)
        plt.yticks(fontsize=38)
        plt.title('Bytes of each column at different points in compression (string, int, compressed)', fontsize=58)
        plt.legend(['string data', 'int data', 'compressed data'], fontsize=38, labelcolor=['lightcoral', 'lightblue', 'lightgreen'])

        pos1 += gap
        pos2 += gap
        pos3 += gap
    # plt.boxplot(data1, positions = [1, 2, 3], notch=None, vert=None, patch_artist=None, widths=None)
    # plt.boxplot(data2, positions = [5, 6, 7], notch=None, vert=None, patch_artist=None, widths=None)
    # plt.boxplot(data3, positions = [9, 10, 11], notch=None, vert=None, patch_artist=None, widths=None)
    plt.savefig('./boxplot.png')


# indata = 0: [
# [[col1: s, i, c][col2, s, i, c][col3, s, i, c]...]
def make_cols_data(strings_data, ints_data, compressed_data):

    num_columns = len(strings_data)
    cols_data = [[] for i in range(num_columns)]
    for col in range(num_columns):
        cols_data[col].append(strings_data[col])
        cols_data[col].append(ints_data[col])
        cols_data[col].append(compressed_data[col])


    return cols_data


s = {0: [150, 100, 110], 1: [160, 165, 170], 2: [150, 100, 110], 3: [150, 100, 110], 4: [174, 160, 167],
     5: [174, 160, 167], 6: [177, 160, 169], 7: [174, 160, 167], 8: [174, 160, 167], 9: [159, 155, 157]}
i = {0: [84, 94, 74], 1: [84, 94, 74], 2: [18, 28, 38], 3: [38, 28, 18], 4: [84, 94, 74], 5: [84, 94, 74],
     6: [84, 94, 74], 7: [84, 94, 74], 8: [84, 94, 74], 9: [84, 94, 74]}
c = {0: [46, 56, 66], 1: [84, 112, 122], 2: [46, 56, 66], 3: [46, 56, 66], 4: [140, 112, 84], 5: [140, 112, 122],
     6: [140, 122, 112], 7: [140, 112, 122], 8: [140, 112, 122], 9: [46, 56, 66]}

# boxplot_bytes_storage(s, i, c)
#s, i, c = boxplot_read_fastp_file('/Users/kristen/PycharmProjects/gwas-compress/scripts/plotting/fastpfor.tsv', 10)
#boxplot_bytes_storage(s, i, c)
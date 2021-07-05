import matplotlib.pyplot as plt

def boxplot_bytes_storage(strings_data, ints_data, compressed_data):
    
    
    pos1 = 1
    pos2 = 2
    pos3 = 3
    gap = 4

    cols_data = make_cols_data(strings_data, ints_data, compressed_data)
    
    for col in range(len(cols_data)):
        plt.boxplot(col, positions = [pos1, pos2, pos3], notch=None, vert=None, patch_artist=None, widths=None)
        pos1 += gap
        pos2 += gap
        pos3 += gap
    #plt.boxplot(data1, positions = [1, 2, 3], notch=None, vert=None, patch_artist=None, widths=None)
    #plt.boxplot(data2, positions = [5, 6, 7], notch=None, vert=None, patch_artist=None, widths=None)
    #plt.boxplot(data3, positions = [9, 10, 11], notch=None, vert=None, patch_artist=None, widths=None)
    plt.savefig('./boxplot.png')



#indata = 0: [
#[[col1: s, i, c][col2, s, i, c][col3, s, i, c]...]
def make_cols_data(strings_data, ints_data, compressed_data):
    print(strings_data, ints_data, compressed_data)
    
    num_columns = len(strings_data)
    cols_data = [[] for i in range(num_columns)]
    i = 0
    for col in range(num_columns):      
        cols_data[col].append(strings_data[col][i])
        cols_data[col].append(ints_data[col][i])
        cols_data[col].append(compressed_data[col][i])
        i += 1

    print(cols_data)

    return cols_data

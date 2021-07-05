import matplotlib.pyplot as plt

def boxplot_bytes_storage(strings_data, ints_data, compressed_data):
    
    
    pos1 = 1
    pos2 = 2
    pos3 = 3
    gap = 4

    cols_data = make_cols_data(strings_data, ints_data, compressed_data)
    
    for col in cols_data:
        p = [pos1, pos2, pos3]
        plt.boxplot(col, positions = p, notch=None, vert=None, patch_artist=None, widths=None)
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
    for col in range(num_columns):
        cols_data[col].append(strings_data[col])
        cols_data[col].append(ints_data[col])
        cols_data[col].append(compressed_data[col])

    print(cols_data)

    return cols_data


s = {0: [150, 150, 150], 1: [162, 162, 162], 2: [150, 150, 150], 3: [150, 150, 150], 4: [174, 160, 167], 5: [174, 160, 167], 6: [177, 160, 169], 7: [174, 160, 167], 8: [174, 160, 167], 9: [159, 155, 157]}
i = {0: [84, 84, 84], 1: [84, 84, 84], 2: [28, 28, 28], 3: [28, 28, 28], 4: [84, 84, 84], 5: [84, 84, 84], 6: [84, 84, 84], 7: [84, 84, 84], 8: [84, 84, 84], 9: [84, 84, 84]}
c = {0: [56, 56, 56], 1: [84, 112, 112], 2: [56, 56, 56], 3: [56, 56, 56], 4: [140, 112, 84], 5: [140, 112, 112], 6: [140, 112, 112], 7: [140, 112, 112], 8: [140, 112, 112], 9: [56, 56, 56]}

boxplot_bytes_storage(s,i,c)
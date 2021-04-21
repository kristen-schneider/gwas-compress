import matplotlib.pyplot as plt

i_file = '/home/krsc0813/projects/gwas-compress/plot_data/codecs_performance-0.tsv'

def main():
    data = get_data(i_file)
    plot_data(data)

def get_data(i_file):
    x = []
    y = []

    f = open(i_file, 'r')
    for line in f:
        A = line.rstrip().split()
        x.append(A[0])
        y.append(float(A[1]))

    return x, y        

def plot_data(data):
    x = data[0]
    y = data[1]
    print(x)
    print(y)
    #y = [1, 2, 4, 5, 6, 8, 2, 3, 4, 5, 6, 7, 8, 9, 11, 1, 3, 5, 2, 3, 8, 3, 13, 3, 4, 8, 2, 4, 9, 7, 8, 3, 11]
    #x = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'sept', 'oct', 'nov', 'dec']
    #y = [31, 28, 100, 40, 65, 82, 12, 90, 34, 43, 87, 20] 

    pos = range(len(x))
    plt.figure(figsize=(15,20))
    plt.bar(x, y, bottom=0)
    plt.xticks(pos, x, rotation=70)
    plt.xlabel('codec')
    plt.ylabel('compression ratio')
    plt.savefig('/home/krsc0813/projects/gwas-compress/plot_data/codecs_plot.png')


if __name__ == '__main__':
    main()

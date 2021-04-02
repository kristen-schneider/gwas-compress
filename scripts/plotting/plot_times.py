import sys
import matplotlib.pyplot as plt

in_file=sys.argv[1]

def main():
    xy = get_xy(in_file)
    #print(xy)
    plot_times(xy)    

def get_xy(in_file):
    f_open = open(in_file)
    x = []
    y = []
    for line in f_open:
        x_y_points = line.rstrip().split()
        x.append(int(x_y_points[0]))
        y.append(int(x_y_points[1]))

    return [x, y]

def plot_times(xy):
    x = xy[0]
    y = xy[1]

    plt.figure(figsize=(15,20))
    plt.plot(x, y, 'b-+')
    plt.title('time to compress file with 1 million lines')
    plt.xlabel('block size (number of lines)')
    plt.ylabel('compression time (seconds)')
    plt.savefig('/scratch/Users/krsc0813/gwas-compress/times.png')

if __name__ == '__main__':
    main()

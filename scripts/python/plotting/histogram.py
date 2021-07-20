import matplotlib.pyplot as plt

f = '/home/krsc0813/projects/gwas-compress/data/ref-alt-all.tsv'

def main():
    #k = [0,0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,4,4,4,5,5,5,6,6,0,0,0,0,0,0,0,2]
    #s = [1,1,1,1,1]
    #plot_histogram(k, s)
    ref_alt_data = get_alt_ref_lengths(f)
    print(max(ref_alt_data[0]), max(ref_alt_data[1]))
    plot_histogram(ref_alt_data[0], ref_alt_data[1])
    
def plot_histogram(ref, alt):
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    axs[0].hist(ref, bins=50)
    axs[0].set_xlabel('reference: length of indel/snp')
    axs[0].set_ylabel('number of rows')
    axs[1].hist(alt, bins=50)
    axs[1].set_xlabel('alternate: length of indel/snp')
    plt.title('Distribution of indel/snp lengths')
    plt.savefig('/home/krsc0813/projects/gwas-compress/plots/indels.png')

def get_alt_ref_lengths(alt_ref_file):
    f = open(alt_ref_file, 'r')
    ref_lengths = []
    alt_lengths = []
    header = ''
    for line in f:
        if header == '': header = line
        else:    
            A = line.rstrip().split()
            ref = A[0]
            ref_lengths.append(len(ref))
            alt = A[1]
            alt_lengths.append(len(alt))

    return(ref_lengths, alt_lengths)
        
    

if __name__ == '__main__':
    main()


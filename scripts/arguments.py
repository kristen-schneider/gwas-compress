from optparse import OptionParser

def get_args():
    parser = OptionParser()

    parser.add_option('--i',
                        dest='i',
                        type=str,
                        help='path to uncompressed, original gwas file')
    parser.add_option('--o',
                        dest='o',
                        type=str,
                        help='path to location of compressed, output file')
    parser.add_option('--b',
                        dest='b',
                        type=int,
                        help='number of rows to be included in each block')

    # this argument might be fixed after parameter sweep
    parser.add_option('--c',
                        dest='c',
                        type=str,
                        nargs='+',
                        help='compression method to be used on the file.')

    # this argument might only be necessary when working with test cases (to allow for reproducibility)
    parser.add_option('--t',
                        dest='t',
                        type=int,
                        help='mtime argument for the gzip compression method')


    return parser.parse_args()

def main():
    args = get_args()
    #print(args.in_text)

if '__name__' == '__main__':
    main()

import argparse

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--i',
                        dest='i',
                        type=str,
                        help='path to uncompressed, original gwas file',
                        required=True)
    parser.add_argument('--o',
                        dest='o',
                        type=str,
                        help='path to location of compressed, output file',
                        required=True)
    parser.add_argument('--b',
                        dest='b',
                        type=int,
                        help='number of rows to be included in each block',
                        required=True)

    # this argument might be fixed after parameter sweep
    parser.add_argument('--c',
                        dest='c',
                        type=str,
                        nargs='+',
                        help='compression method to be used on the full file',
                        required=True)

    # this argument might only be necessary when working with test cases (to allow for reproducibility)
    parser.add_argument('--t',
                        dest='t',
                        type=int,
                        help='mtime argument for the gzip compression method',
                        required=False)


    return parser.parse_args()

def main():
    args = get_args()
    #print(args.in_text)
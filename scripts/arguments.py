import argparse

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--in_txt',
                        dest='in_txt',
                        type=str,
                        help='path to txt file with all directories storing mean_per_tech_combo results',
                        required=True)

    return parser.parse_args()

def main():
    args = get_args()
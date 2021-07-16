import configparser

def main():
    config_to_args()
    #get_args_from_config()

def get_args_from_config(machine):
    c = config_to_args()

    args = dict()
    for arg in c[machine]:
        args[arg] = c[machine][arg]
    # print(args)
    return args

def config_to_args():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config

if __name__ == '__main__':
    main()

import configparser

def main():
    config_to_args()
    #get_args_from_config()

def get_args_from_config(machine, config_file):
    c = config_to_args(config_file)

    args = dict()
    for arg in c[machine]:
        args[arg] = c[machine][arg]
    # print(args)
    return args

def config_to_args(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    #config.read('/home/krsc0813/projects/gwas-compress/config_files/config.ini')

    return config

if __name__ == '__main__':
    main()

import sys, getopt, random


def random_sting(seed, len_bytes: int) -> bytes:
    random.seed(seed)
    return bytes([random.getrandbits(8) for _ in range(0, len_bytes)])


def main(script_path, argv):
    help_str = 'file_gen.py -l <length (bytes)> -n <file name> -s <random_seed>'
    len_bytes = ''
    file_name = ''
    seed = ''
    sep = '/'
    try:
        opts, args = getopt.getopt(argv, "hl:n:s:", ["len=", "fname=", "seed="])
    except getopt.GetoptError:
        print(help_str)
        exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-l", "--len"):
            len_bytes = arg
            len_bytes = int(len_bytes)
        elif opt in ("-n", "--fname"):
            file_name = arg
        elif opt in ("-s", "--seed"):
            seed = arg
    with open(file_name, 'wb+') as file_to_write:
        file_to_write.write(random_sting(seed, len_bytes))


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
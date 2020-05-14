import os
import logging
import sys
import getopt
import time
import threading


class ShellProbe:
    """
    mon_name : str - probe name
    script_dir : str - path to probes script
    log_path : str - path to probe journal
    check_interval : float - interval behind stat check
    exec_string=None : str - CLI command returned observation parameter
    parse_function=lambda x: x : function, returned parsed parameter like stat1;stat2;stat3;
    """
    def __init__(self, mon_name: str,
                 script_dir: str,
                 log_path: str,
                 check_interval: float,
                 exec_string: str = None,
                 parse_function=lambda x: x):
        self.mon_name = mon_name
        self.check_interval = check_interval
        self.exec_string = exec_string
        self.parse_function = parse_function
        self.log_formatter = logging.Formatter('%(asctime)s;%(name)s;%(message)s')
        self.script_dir = script_dir
        self.log_filename = log_path + mon_name + ".csv"

    def start_serving(self):
        log = logging.getLogger(self.mon_name)
        log.setLevel(level=logging.INFO)
        fh = logging.FileHandler(self.log_filename)
        fh.setLevel(level=logging.INFO)
        fh.setFormatter(self.log_formatter)
        log.addHandler(fh)

        while(True):
            if self.exec_string is not None:
                stream = os.popen(self.exec_string)
            else:
                stream = os.popen(f'sh {self.script_dir}{self.mon_name}.sh')
            output = stream.read()
            output = self.parse_function(output)
            log.info(output)
            time.sleep(self.check_interval)


def iostat_cpu_parser(input_string):
    input_string = input_string.replace("\n", '').split(' ')
    tmp_arr = []
    for i in range(len(input_string)):
        if input_string[i] != '':
            tmp_arr.append(input_string[i])
    return ';'.join(tmp_arr)


def iostat_disk_parser(input_string):
    input_string = input_string.replace("\n", ' ').split(' ')
    tmp_arr = []
    for i in range(len(input_string)):
        if input_string[i] != '':
            tmp_arr.append(input_string[i])
    return ';'.join(tmp_arr)


def free_mem_parser(input_string):
    input_string = input_string.replace("\n", ' ').split(' ')
    tmp_arr = []
    for i in range(len(input_string)):
        if input_string[i] != '':
            tmp_arr.append(input_string[i].replace(':', ''))
    return ';'.join(tmp_arr)


def main(argv):
    sep = os.sep
    script_path = argv[0]
    log_path = (sep.join(str(script_path).split(sep)[:-1])) + sep
    script_path = log_path
    help_str = f'{str(argv[0]).split(os.sep)[-1]} -p <path to log folder>, -s <path to monitor script folder>\n\
Default (script path): {log_path}'

    try:
        opts, args = getopt.getopt(argv[1:], "hp:s:", ["path=", "scdir="])
    except getopt.GetoptError:
        print(f"Used default value(script folder): {log_path}")
        opts = [("", "")]
        # exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-p", "--path"):
            if arg[-1] == sep:
                log_path = arg
            else:
                log_path = arg + sep
        elif opt in ("-s", "--scdir"):
            if arg[-1] == sep:
                script_path = arg
            else:
                script_path = arg + sep

    testfile = log_path+"test"

    try:
        with open(testfile, 'w') as file:
            file.write('42')
    except Exception as e:
        print(f"Unable to write file: {e}")
        exit(2)
    else:
        os.remove(testfile)

    # check time (second)
    check_cpu = 0.01
    check_disk = 1
    check_network = 0.1
    check_mem =  0.01
    check_proc = 0.1

    mon_dict={
        'mon_cpu': threading.Thread(target=ShellProbe('mon_cpu',
                                                      script_path,
                                                      log_path,
                                                      check_cpu,
                                                      exec_string="sh -c 'iostat -c | head -n 4 | tail -n 1'",
                                                      parse_function=iostat_cpu_parser
                                                      ).start_serving, args=()),
        'mon_disk': threading.Thread(target=ShellProbe('mon_disk',
                                                       script_path,
                                                       log_path,
                                                       check_disk,
                                                       exec_string="sh -c 'iostat | grep -v 'loop' | tail -n +7'",
                                                       parse_function=iostat_disk_parser,
                                                       ).start_serving, args=()),
        'mon_mem': threading.Thread(target=ShellProbe('mon_mem',
                                                      script_path,
                                                      log_path,
                                                      check_mem,
                                                      exec_string="sh -c 'free | grep -E \"^Mem|Swap\"'",
                                                      parse_function=free_mem_parser,
                                                      ).start_serving, args=()),
        'mon_network': threading.Thread(target=ShellProbe('mon_network',
                                                          script_path,
                                                          log_path,
                                                          check_network,
                                                          exec_string="sh -c 'for i in `ifconfig | \
                                                          grep -oE \"^[a-zA-Z0-9-]*\"`; do echo $i; \
                                                          ifconfig $i | grep -oE \"(RX|TX) packets(\s|\:)[0-9]*\"; \
                                                          done'",
                                                          parse_function=lambda x : x.replace("\n", ' ')\
                                                                                        .replace(':', '')\
                                                                                        .replace('RX packets', '')\
                                                                                        .replace('TX packets', '')\
                                                                                        .replace('  ', ' ')\
                                                                                        .replace(' ', ';')
                                                          ).start_serving, args=())
    }

    for key in mon_dict.keys():
        mon_dict[key].start()

    for key in mon_dict.keys():
        mon_dict[key].join()


if __name__ == '__main__':
    main(sys.argv)

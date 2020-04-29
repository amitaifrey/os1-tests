#!/usr/bin/python3

import signal
import subprocess
import argparse
import time
import re
import difflib
import os
import shutil

TEST_DIR = '/tmp/smash_test'

FILES_TO_COPY = ["random1.txt", "random2.txt",  "my_sleep"]

UNIT = [
    "unit/cd",
    "unit/chprompt",
    "unit/jobs",
    "unit/manual_pid",
    "unit/quit",
    "unit/redirect",
    "unit/showpid",
    "unit/timeout",
    "unit/kill",
    "unit/pipe",
]

def prepare_env():
    testsdir = os.path.dirname(os.path.abspath(__file__))
    if testsdir != '' :
        testsdir = testsdir + "/files/"
    
    os.system("killall -9 sleep 2> /dev/null")
    # Compile my_sleep
    os.system(f"gcc -o {testsdir}my_sleep {testsdir}my_sleep.c")

    try:
        shutil.rmtree(TEST_DIR)
    except:
        pass
    
    try:
        os.mkdir(TEST_DIR)
        os.mkdir(TEST_DIR + '/sub1')
        os.mkdir(TEST_DIR + '/sub2')
        os.mkdir(TEST_DIR + '/sub3')
        os.mkdir(TEST_DIR + '/sub1/subsub1')
        os.mkdir(TEST_DIR + '/sub2/subsub2')
        os.mkdir(TEST_DIR + '/sub1/subsub1/last')
    except:
        pass

    try:
        for file in FILES_TO_COPY:
            dest_path = TEST_DIR + "/" + file
            shutil.copyfile(testsdir + file, dest_path)
            os.chmod(dest_path, 511)
    except:
        print("Warning, failed to copy files")

    print("Setup is done.")

def run_test(execu, test, valgrind):
    input = test + ".in"
    output = test + ".out"

    prepare_env()

    o = open(output, "w")
    i = open(input, 'r')

    smash_abs_path = os.path.abspath(execu)
    exec_args = [smash_abs_path]

    valgrind_path = os.getcwd() + '/' + test + '.mem'
    if valgrind:
        exec_args = ['valgrind', '-v', '--leak-check=full', '--log-file=' + valgrind_path, smash_abs_path]

    p = subprocess.Popen(exec_args, stdin=subprocess.PIPE,
                            stdout=o, stderr=subprocess.STDOUT, cwd=TEST_DIR)

    time.sleep(1)
    for line in i.readlines():
        time.sleep(0.1)
        if line.startswith('#'):
            continue
        if line.startswith('CtrlZ'):
            p.send_signal(signal.SIGTSTP)
            continue
        if line.startswith('CtrlC'):
            p.send_signal(signal.SIGINT)
            continue
        if line.startswith("!"):
            exec(line[1:])
            continue
        p.stdin.writelines([bytes(line, "utf-8")])
        try:
            p.stdin.flush()
        except:
            pass

    time.sleep(3) 
    try:
        p.stdin.close()
    except:
        pass
    i.close()
    o.close()

    if valgrind:
        with open(valgrind_path) as f:
            for line in f:
                if 'All heap blocks were freed -- no leaks are possible' in line:
                    print('no leaks')
                    return
            print('leak detected')


def unified_diff(a, b, n=3):
    for group in difflib.SequenceMatcher(None,a,b).get_grouped_opcodes(n):
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                continue
            if tag == 'replace':
                for i in range(0,min(i2-i1,j2-j1)):
                    if not re.match(a[i1], b[j1]):
                        yield '-' + a[i1] + '\n'
                        yield '+' + b[j1] + '\n'
                    i1 += 1
                    j1 += 1
                while(i1 < i2):
                    yield '-' + a[i1] + '\n'
                    i1 += 1
                while(j1 < j2):
                    yield '+' + b[j1] + '\n'
                    j1 += 1
            if tag == 'delete':
                for line in a[i1:i2]:
                    yield '-' + line + '\n'
            if tag == 'insert':
                for line in b[j1:j2]:
                    yield '+' + line + '\n'


def diff(expected, actual):
    e = open(expected, 'r')
    a = open(actual, 'r')
    d = unified_diff([x.rstrip() for x in e.readlines()], [x.rstrip() for x in a.readlines()])
    diff_str = ''.join(d)
    if diff_str == '':
        print('Files are equal')
    else:
        print('Files are different')
        print(diff_str)
    a.close()
    e.close()

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-smash', type=str, default="./smash")
    parser.add_argument('-test', type=str)
    parser.add_argument('-valgrind', type=str2bool, default=False)
    args = parser.parse_args()

    output = args.test + ".out"
    exp = args.test + ".exp"

    if args.test == "all" or args.test == "unit":
        for test in UNIT:
            print(test + ": ", end='')
            run_test(args.smash, test, args.valgrind)
            output = test + ".out"
            exp = test + ".exp"
            diff(exp, output)

    if args.test == "all" or args.test == "random":
        for i in range(1,11):
            test = 'random/test' + str(i)
            print(test + ": ", end='')
            run_test(args.smash, test, args.valgrind)
            output = test + ".out"
            exp = test + ".exp"
            diff(exp, output)

    if args.test != "all" and args.test != "random" and \
            args.test != "unit":
        run_test(args.smash, args.test, args.valgrind)
        diff(exp, output)

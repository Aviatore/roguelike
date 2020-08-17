import sys
import os
import random


def key_pressed():
    try:
        import tty, termios
    except ImportError:
        try:
            # probably Windows
            import msvcrt
        except ImportError:
            # FIXME what to do on other platforms?
            raise ImportError('getch not available')
        else:
            key = msvcrt.getch().decode('utf-8')
            return key
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def clear_screen():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


def read_csv(file_name):
    output = []
    
    with open(file_name, 'r') as file:
        for line in file:
            line = line.rstrip()
            line_splitted = line.split(',')
            output.append(line_splitted)

    return output

people_data = read_csv('people_names.csv')
a = random.sample(people_data, 1)
print(a)
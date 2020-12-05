import time

def measure(fn):
    start = time.time()
    fn()
    return time.time() - start

def readfile(file, separator = None):
    lines = []
    with open(file) as fp:
        for line in fp.readlines():
            line = line.strip()
            if separator:
                line = line.split(separator)
            lines.append(line)
    return lines

def remove_empty(lst):
    return list(filter(None, lst))
import re


def read_file(fn):
    # Read file line-by-line and store in list
    with open(fn, 'r') as f:
        lines = [line.rstrip() for line in f]
    print(f'Number of Conversations is: {len(lines)}')
    return lines


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    k = [tryint(c) for c in re.split('([0-9]+)', s)]
    return k


def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l


def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

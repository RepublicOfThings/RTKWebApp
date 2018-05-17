import numpy as np
from datetime import datetime
import re


def alpha_numeric(string, omit=[], lower=False):
    string = string.replace('\n', ' ').replace('\r', '').replace('\t', '')
    p = re.compile(r'[^a-zA-Z0-9]')
    string = p.sub('', string)
    if lower:
        string = string.lower()
    frags = [x for x in string.split() if x not in omit]
    return ' '.join(frags)


def time_stamp(fmt="%d-%m-%Y %H:%M:%S"):
    return datetime.now().strftime(fmt)


def unique_integer(data):
    data = list(data)
    i = 0
    while (i in data):
        i += 1
    return i


def confidence():  # ?
    c = np.random.rand()
    if c < 0.5:
        c += 0.5
    return c
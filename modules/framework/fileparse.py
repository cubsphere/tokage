import re
from typing import List

from modules.framework.timedsample import TimedSample

def __checklen(split: List[str], i:int, s: str):
    length = len(split)
    if length != 3:
        exit(f"error reading line {i} of infile:\n{s}")

def __sample_or_exit(i: int, s: str) -> TimedSample:
    split = re.split(r"\W+", s)
    __checklen(split, i, s)
    try:
        num = int(split[0])
        req = int(split[1])
        res = int(split[2])
    except ValueError:
        raise ValueError(f"error reading line {i} of infile:\n{s}\nfailed to parse int")
    if num < 0 or num >= 2147483647:
        raise ValueError(f"error reading line {i} of infile:\n{s}\n{str(num)} outside of permitted range")
    elif res < req:
        raise ValueError(f"error reading line {i} of infile:\n{s}\response time ({res}) cannot be less than request time ({req})")
    return TimedSample(num, req, res)

def samples_from_file(f) -> List[TimedSample]:
    lines = [s.strip() for s in f if s.strip() != ""]
    samples = [__sample_or_exit(i, s) for i, s in enumerate(lines)]
    f.close()
    if len(samples) < 2:
        raise ValueError("input file must have at least two timestamp-number pairs")
    return samples
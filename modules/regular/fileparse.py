import re
from typing import List

def __linetonum(i: int, s: str, three_nums: bool) -> int:
    try:
        split = re.split(r"\W+",s)
        if three_nums and len(split) != 3:
            raise ValueError(f"error reading line {i} of infile:\n{s}\nexpected 3 nums, found {len(split)}")
        elif (not three_nums) and len(split) != 1:
            raise ValueError(f"error reading line {i} of infile:\n{s}\nexpected 1 num, found {len(split)}")
        num = int(re.split(r"\W+",s)[0])
        if num < 0 or num >= 2147483647:
            raise ValueError(f"error reading line {i} of infile:\n{s}\n{str(num)} outside of permitted range")
        return num
    except ValueError:
        raise ValueError(f"error reading line {i} of infile:\n{s}\nfailed to parse int")

def samples_from_file(f) -> List[int]:
    lines = [s.strip() for s in f if s.strip() != ""]
    three_nums = False
    length = len(re.split(r"\W+", lines[0]))
    if length == 1:
        pass
    elif length == 3:
        three_nums = True
    else:
        raise ValueError("infile in unrecognized format (need either 1 or 3 numbers per line)")

    samples = [__linetonum(i, s, three_nums) for i, s in enumerate(lines)]
    if len(samples) < 55:
        raise ValueError("need at least 55 samples in infile")
    return samples
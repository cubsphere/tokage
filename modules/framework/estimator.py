from typing import List
from operator import itemgetter

from modules.framework.timedsample import TimedSample

def estimate(samples: List[TimedSample], target_req: int, target_res: int, amount: int, leniency: int):
    basesamp = samples[0]
    sip = __determine_seed_positive(samples, leniency)
    
    listy = []
    baseval = basesamp.num
    timerange = (target_req - basesamp.res - leniency, target_res - basesamp.req + leniency)
    timecentre = (target_req + target_res - basesamp.req - basesamp.res)//2
    bottom = False
    top = False
    i = 0
    while i < amount:
        if (bottom and top):
            break
        dist = __spiral(timecentre, i)
        i += 1
        if dist < timerange[0]:
            bottom = True
            continue
        if dist > timerange[1]:
            top = True
            continue
        listy.append(__prediction_for(baseval, dist, sip))
    
    return listy[:amount]

def __determine_seed_positive(samples: List[TimedSample], leniency: int) -> bool:
    base = samples[0]
    target = samples[1]
    for b in [True, False]:
        if __find_seed_diff(base, target, b, leniency) != None:
            return b
    __no_rel()

def __find_seed_diff(base: TimedSample, target: TimedSample, sip: bool, leniency: int) -> int:
    baseval = base.num
    timerange = (target.req - base.res - leniency, target.res - base.req + leniency)
    timecentre = (target.req + target.res - base.req - base.res)//2
    diff = None
    bottom = False
    top = False
    i = 0
    while True:
        if (bottom and top):
            break
        dist = __spiral(timecentre, i)
        i += 1
        if dist < timerange[0]:
            bottom = True
            continue
        if dist > timerange[1]:
            top = True
            continue
        if abs(__prediction_for(baseval, dist, sip) - target.num) < 1:
            diff = dist
            break
    return diff
    
def __no_rel():
    raise ValueError(
        "could not find relationship between samples in input file\n" +
        "try increasing leniency (-l) or obtaining new samples"
    )

def __spiral(centre: int, dist: int) -> int:
    dist += 1
    even = dist % 2 == 0
    sign = 1 if even else -1
    return centre + dist//2 * sign

def __prediction_for(baseval: int, diff: int, seed_is_positive: bool) -> int:
    step = 1121899819 if seed_is_positive else 1025583828
    return (baseval + diff * step) % 2147483647
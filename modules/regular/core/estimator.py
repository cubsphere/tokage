from typing import List

def singlethread_estimate(samples: List[int], amount: int) -> List[int]:
    retlist = []
    for a in range(amount):
        i = a % 55
        j = (i + 21) % 55
        samples[i] = (samples[i] - samples[j] + 1559595546 + 2147483647) % 2147483647
        retlist.append(samples[i])
    return retlist

def alwaysnew_estimate(samples: List[int], amount: int) -> List[int]:
    retlist = []
    for a in range(amount):
        i = a % 55
        j = (i + 21) % 55
        samples[i] = (samples[i] - samples[j] + 1559595546 * (1121899819 + 1)) % 2147483647
        retlist.append(samples[i])
    return retlist
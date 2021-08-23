from typing import List

def estimate(samples: List[int], amount: int) -> List[int]:
    retlist = []
    for a in range(amount):
        i = a % 55
        j = (i + 21) % 55
        samples[i] = (samples[i] - samples[j] + 2147483647) % 2147483647
        retlist.append(samples[i])
    return retlist
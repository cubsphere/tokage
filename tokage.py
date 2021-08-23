import io
from typing import List
from enum import Enum

from modules.args import get_args

from modules.framework.fileparse import samples_from_file as fw_samples_from_file
from modules.framework.estimator import estimate as fw_estimate

from modules.regular.fileparse import samples_from_file
from modules.regular.core.estimator import singlethread_estimate, alwaysnew_estimate

from modules.regular.common.estimator import estimate as common_estimate

class TokageMode(Enum):
    COMMON = 1
    CORE_1THREAD = 2
    CORE_ALWAYSNEW = 3
    FRAMEWORK = 4


def run(
        infile, mode: TokageMode,
        amount: int = 1000,
        target_reqtime: int = None, target_restime: int = None, leniency: int = 50
    ) -> List[int]:
        if mode == TokageMode.COMMON:
            samples = samples_from_file(infile)
            guesses = common_estimate(samples[len(samples) - 55:], amount)
            return guesses
        elif mode == TokageMode.CORE_1THREAD:
            samples = samples_from_file(infile)
            guesses = singlethread_estimate(samples[len(samples) - 55:], amount)
            return guesses
        elif mode == TokageMode.CORE_ALWAYSNEW:
            samples = samples_from_file(infile)
            guesses = alwaysnew_estimate(samples[len(samples) - 55:], amount)
            return guesses
        elif mode == TokageMode.FRAMEWORK:
            samples = __prepare_fw_samples(infile, target_reqtime, target_restime)
            guesses = fw_estimate(samples, target_reqtime, target_restime, amount, leniency)
            return guesses
        else:
            raise ValueError(f"unrecognized prediction mode {mode}")


def __prepare_fw_samples(infile, target_reqtime: int, target_restime: int) -> list:
    if target_reqtime == None or target_restime == None:
        raise ValueError(f"arguments target_reqtime (-q) and target_restime (-r) must be specified if running .NET Framework prediction mode")
    samples = fw_samples_from_file(infile)
    if (target_restime < target_reqtime):
        raise ValueError(f"target_restime ({target_restime}) cannot be less than target_reqtime ({target_reqtime})")
    return samples


def __target_to_tokage_mode(s: str) -> TokageMode:
    if s == "c":
        return TokageMode.COMMON
    elif s == "s":
        return TokageMode.CORE_1THREAD
    elif s == "n":
        return TokageMode.CORE_ALWAYSNEW
    elif s == "f":
        return TokageMode.FRAMEWORK
    else:
        raise ValueError(f"unrecognized prediction target {s}")

def main():
    args = get_args()
    mode = __target_to_tokage_mode(args.target)
    with open(args.infile) as f:
        guesses = run(
            f, mode,
            args.amount,
            args.target_reqtime, args.target_restime, args.leniency
        )
    for g in guesses:
        print(g)

if __name__ == "__main__":
    main()
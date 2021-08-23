########################################
#                                      #
#            CONFIGURATION             #
#                                      #
########################################

outfile = "outfile.json"
output_raw_data = True

print_at_checkpoints = True

core_executable_path      = r"path/to/TokageVulnExample/net5.0/TokageVulnExample.exe"
framework_executable_path = r"path/to/TokageVulnExample/net48/TokageVulnExample.exe"

common_case_confs = [
    # number_of_runs, numbers_to_check
    (50             , 55),
]

core_run_confs = [
    # number_of_runs, numbers_to_check, always_new
    (50             , 55              , False),
    (50             , 55              , True ),
]

fw_run_confs = [
    #                 (ms)      (ms)
    # number_of_runs, lag_mean, lag_std, leniency
    (50             , 0       , 0      , 50),
    (50             , 20      , 10     , 50),
    (50             , 40      , 20     , 50),
    (50             , 60      , 30     , 50),
    (50             , 80      , 40     , 50),
    (50             , 100     , 50     , 50),
    (50             , 120     , 60     , 50),
    (50             , 140     , 70     , 50),
    (50             , 160     , 80     , 50),
    (50             , 180     , 90     , 50),
    (50             , 200     , 100    , 50),
]

# constants
N_SAMPLES = 2
COMMON = 0
SINGLE_THREAD = 1
ALWAYS_NEW = 2

# imports

import random
import math
import time
import subprocess
import statistics
import io
import os
import json
import requests

from typing import List

from tokage import run, TokageMode
from modules.framework.timedsample import TimedSample


########################################
#                                      #
#                 MAIN                 #
#                                      #
########################################

def main():
    t = time.time()
    results = []
    # .net framework tests
    for n_runs, mean, std, leniency in fw_run_confs:
        sim_results = fw_runs(n_runs, mean, std, leniency)
        m = statistics.mean(sim_results)
        s = statistics.stdev(sim_results)
        d = 2.576 * s / math.sqrt(len(sim_results))
        ci99 = (m - d, m + d)
        result = {
            "env": ".NET Framework 4.8",
            "n_runs": n_runs,
            "lag_mean": mean,
            "lag_std":  std,
            "leniency": leniency,
            "runs_mean": statistics.mean(sim_results),
            "runs_ci99": ci99,
        }
        if output_raw_data:
            result["raw_data"] = sim_results
        results.append(result)

    # .net core/5.0 tests
    for n_runs, n_tocheck, always_new in core_run_confs:
        sim_results = core_runs(n_runs, n_tocheck, always_new)
        accuracy = statistics.mean(sim_results)
        result = {
            "env": ".NET 5.0",
            "use_case": ("always new" if always_new else "single-threaded"),
            "n_runs": n_runs,
            "n_checked": n_tocheck,
            "accuracy": accuracy,
        }
        if output_raw_data:
            result["raw_data"] = sim_results
        results.append(result)

    # common case tests
    for n_runs, n_tocheck in common_case_confs:
        sim_results = core_runs(n_runs, n_tocheck, always_new)
        accuracy = statistics.mean(sim_results)
        result = {
            "env": ".NET 5.0",
            "n_runs": n_runs,
            "n_checked": n_tocheck,
            "accuracy": accuracy,
        }
        if output_raw_data:
            result["raw_data"] = sim_results
        results.append(result)
    
    j = json.dumps(results, indent = 4)
    t = time.time() - t
    print(f"{t} seconds elapsed")
    with open(outfile, "w") as fi:
        fi.write(j)
    return


########################################
#                                      #
#   COMMON/SINGLE INSTANCE CASE TESTS  #
#                                      #
########################################

def common_runs(n_runs: int, n_tocheck: int) -> List[int]:
    handle = None
    try:
        handle = subprocess.Popen([
            core_executable_path,
            "-s"],
            cwd=os.path.dirname(core_executable_path)
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"could not find net5.0 TokageVulnExample.exe at {core_executable_path}\n"
        )
    
    results = []
    session = requests.Session()
    for i in range(n_runs):
        if print_at_checkpoints and i % 10 == 0:
            print(f"common: {i}-th run, {n_tocheck} to check")
        samples = common_native_samples(session)
        targets = [common_native_rand(session) for _ in range(n_tocheck)]
        s = ""
        for sam in samples:
            s += f"{sam}\n"
        s = io.StringIO(s)
        guesses = run(s, TokageMode.COMMON, amount = n_tocheck)
        run_results = [1 if g == t else 0 for (g, t) in zip(guesses, targets)]
        results.append(statistics.mean(run_results))
    
    handle.kill()
    # wait to make sure it's really dead
    time.sleep(1)
    return results

def common_native_samples(session) -> List[int]:
    return [common_native_rand(session) for _ in range(55)]

def common_native_rand(session) -> int:
    r = session.get("http://localhost:8080/sample")
    if (r.status_code != 200):
        raise EnvironmentError("error fetching samples")
    return int(r.text)

########################################
#                                      #
#          .NET 5.0/CORE TESTS         #
#                                      #
########################################

def core_runs(n_runs: int, n_tocheck: int, always_new: bool) -> List[int]:
    handle = None
    mode = TokageMode.CORE_ALWAYSNEW if always_new else TokageMode.CORE_1THREAD
    try:
        handle = subprocess.Popen([
            core_executable_path,
            "-n" if always_new else ""],
            cwd=os.path.dirname(core_executable_path)
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"could not find net5.0 TokageVulnExample.exe at {core_executable_path}\n"
        )
    
    results = []
    session = requests.Session()
    for i in range(n_runs):
        if print_at_checkpoints and i % 10 == 0:
            print(f"core: {i}-th run, {n_tocheck} to check, " +("always-new" if always_new else "single-threaded"))
        samples = core_native_samples(session)
        targets = [core_native_rand(session) for _ in range(n_tocheck)]
        s = ""
        for sam in samples:
            s += f"{sam}\n"
        s = io.StringIO(s)
        guesses = run(s, mode, amount = n_tocheck)
        run_results = [1 if g == t else 0 for (g, t) in zip(guesses, targets)]
        results.append(statistics.mean(run_results))

    handle.kill()
    # wait to make sure it's really dead
    time.sleep(1)
    return results

def core_native_samples(session) -> List[int]:
    return [core_native_rand(session) for _ in range(55)]

def core_native_rand(session) -> int:
    r = session.get("http://localhost:8080/sample")
    if (r.status_code != 200):
        raise EnvironmentError("error fetching samples")
    return int(r.text)

########################################
#                                      #
#         .NET FRAMEWORK TESTS         #
#                                      #
########################################

def fw_runs(n_runs: int, mean:float, std: float, leniency: int) -> List[int]:
    handle = None
    session = requests.Session()
    amount = 400 + mean * 2 + std * 20
    try:
        handle = subprocess.Popen([
            framework_executable_path,
            "-m", str(mean), "-d", str(std)],
            cwd=os.path.dirname(framework_executable_path)
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"could not find net48 TokageVulnExample.exe at {framework_executable_path}\n"
        )
    results = []
    for i in range(n_runs):
        if print_at_checkpoints and i % 100 == 0:
            print(f"framework: {i}-th run, {mean} mean, {std} std")
        samples, target_reqtime, target_restime, target_val = fw_samples_and_target(N_SAMPLES, session)
        s = ""
        for sam in samples:
            s += f"{sam.num} {sam.req} {sam.res}\n"
        s = io.StringIO(s)
        estimates = run(
            s,
            TokageMode.FRAMEWORK,
            target_reqtime=target_reqtime,
            target_restime=target_restime,
            amount=amount,
            leniency=leniency
        )
        index = estimates.index(target_val) if target_val in estimates else -1
        results.append(index)
    handle.kill()
    # wait to make sure it's really dead
    time.sleep(1)
    return results

def fw_rand(session) -> int:
    r = session.get("http://localhost:8080/sample")
    if (r.status_code != 200):
        raise EnvironmentError("error fetching samples")
    return int(r.text)


def fw_samples_and_target(n_samples: int, session):
    wait_for_server_OK(session)
    samples = []
    for _ in range(n_samples):
        req = int(time.time()*1000)
        value = fw_rand(session)
        res = int(time.time()*1000)
        sample = TimedSample(value, req, res)
        samples.append(sample)
        time.sleep(0.05)
    target_reqtime = int(time.time()*1000)
    target_val = fw_rand(session)
    target_restime = int(time.time()*1000)
    return samples, target_reqtime, target_restime, target_val

# the server needs some time for setup
# making a request guarantees the server will be up and ready when the response is received.
def wait_for_server_OK(session):
    fw_rand(session)

################
# calling main #
################
if __name__ == "__main__":
    main()
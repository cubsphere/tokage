```
usage: tokage.py [-h] [-a AMOUNT] [-q TARGET_REQTIME] [-r TARGET_RESTIME] [-l L] infile target

a tool for cracking C# System.Random number generation

positional arguments:
  infile                path to input file with sampled numbers. contents must be in the following format:
                        [number1] [req1_timestamp] [res1_timestamp]
                        [number2] [req2_timestamp] [res2_timestamp]
                        ...
                        (timestamps are only needed for .NET Framework prediction, and are otherwise optional and unused)
  target                target environment/use case. avaialable options:
                        c: target the common use case. works against any .NET environment. requires at least [55] samples in infile
                        s: target single-threaded generation on .NET Core or .NET 5+. requires at least [55] samples in infile
                        n: target always-new-threaded generation on .NET Core or .NET 5+. requires at least [55] samples in infile
                        f: target .NET Framework. requires at least [2] samples in infile. also requires -q, -r, and timestamps in infile

optional arguments:
  -h, --help            show this help message and exit
  -a AMOUNT, --amount AMOUNT
                        amount of guesses to output. default is 1000
  -q TARGET_REQTIME, --target_reqtime TARGET_REQTIME
                        target sample request time, used only in .NET Framework prediction
  -r TARGET_RESTIME, --target_restime TARGET_RESTIME
                        target sample response time, used only in .NET Framework prediction
  -l L, --leniency L    maximum clock error leniency (ms), used only in .NET Framework prediction. default is 50
```
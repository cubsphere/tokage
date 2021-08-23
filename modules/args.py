import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description = 
            "a tool for cracking C# System.Random number generation\n"
            "\n",
        formatter_class = argparse.RawTextHelpFormatter
    )
    
    #obligatory args
    parser.add_argument(
        "infile",
        help =
            "path to input file with sampled numbers. contents must be in the following format:\n"
            "[number1] [req1_timestamp] [res1_timestamp]\n"
            "[number2] [req2_timestamp] [res2_timestamp]\n"
            "...\n"
            "(timestamps are only needed for .NET Framework prediction, and are otherwise optional and unused)\n",
        type = str    
    )
    parser.add_argument(
        "target",
        help =
            "target environment/use case. avaialable options:\n"
            "c: target the common use case. works against any .NET environment. requires at least [55] samples in infile\n"
            "s: target single-threaded generation on .NET Core or .NET 5+. requires at least [55] samples in infile\n"
            "n: target always-new-threaded generation on .NET Core or .NET 5+. requires at least [55] samples in infile\n"
            "f: target .NET Framework. requires at least [2] samples in infile. also requires -q, -r, and timestamps in infile\n",
        type = str
    )

    #optional args
    parser.add_argument(
        "-a", "--amount",
        default = 1000,
        help = "amount of guesses to output. default is 1000",
        type = int
    )
    parser.add_argument(
        "-q", "--target_reqtime",
        default = None,
        help = "target sample request time, used only in .NET Framework prediction\n",
        type = int
    )
    parser.add_argument(
        "-r", "--target_restime",
        default = None,
        help = "target sample response time, used only in .NET Framework prediction\n",
        type = int
    )
    parser.add_argument(
        "-l", "--leniency",
        metavar = "L",
        default = 50,
        help = "maximum clock error leniency (ms), used only in .NET Framework prediction. default is 50",
        type = int
    )
    return parser.parse_args()
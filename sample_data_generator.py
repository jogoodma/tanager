#!/usr/bin/env python3
import argparse
from random import gauss
import statistics as stats

# Create the parser
parser = argparse.ArgumentParser(
    prog='sample_data_generator',
    usage='%(prog)s [options] path',
    description='Tanager sample data generator.')

parser.add_argument('-generations', type=int, default=10, help="Number of generations.")
parser.add_argument('-popsize', type=int, default=10, help="Population size.")
parser.add_argument('-solution', type=float, default=1.0, help="Starting solution.")
parser.add_argument('-stdev', type=float, default=0.03, help="Starting standard deviation.")

if __name__ == '__main__':
    args = parser.parse_args()

    solution = args.solution
    stdev = args.stdev

    print("generation", end='\t')
    [print(f'i_{i}', end='\t') for i in range(1, args.popsize+1)]
    print('mean\tstdev')

    for i in range(1, args.generations + 1):
        print(i, end='\t')
        pop_vals = []
        for j in range(1, args.popsize + 1):
            val = gauss(solution, stdev)
            pop_vals.append(val)
            print(f'{val:.6f}', end='\t')
        print(f'{stats.fmean(pop_vals):.6f}', f'{stats.stdev(pop_vals):.6f}', sep='\t')
        solution = solution * 0.67
        stdev = stdev * 0.75


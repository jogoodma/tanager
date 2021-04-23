import glob
import os.path as path

import numpy as np
import pandas as pd


def num_generations(pathname: str = None):
    stats_path = path.join(pathname, 'tanager-statistics-file.csv')
    stats_file = glob.glob(stats_path, recursive=False)[0]

    if stats_file is not None:
        try:
            with open(stats_file, 'r') as fh:
                last_line = fh.readlines()[-1]
                return int(last_line.split(',')[0])
        except IOError as e:
            print(f'Caught an IOError while trying to find max generations in {pathname}: {e}')
        except ValueError as e:
            print(f'Caught a ValueError while trying to find max generations in {pathname}: {e}')
    return 0


def slider_round(x, base=5):
    return base * round(x / base)


def load_data_files(pathname: str = None):
    if pathname is not None:
        print("Loading all data frames.")
        stats_file = path.join(pathname, 'tanager-statistics-file.csv')
        individuals_file = path.join(pathname, 'tanager-individuals-file.csv')
        return {
            'statistics': pd.read_csv(stats_file),
            'individuals': pd.read_csv(individuals_file)
        }
    return None


def filter_generation(df: pd.DataFrame, generation_filter: tuple = (np.NINF, np.inf)):
    if generation_filter:
        return df[df.generation.between(generation_filter[0], generation_filter[1])]
    return df

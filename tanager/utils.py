import glob
import os.path as path


def num_generations(pathname: str = None):
    stats_path = path.join(pathname, 'tanager-statistics-file-*.csv')
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

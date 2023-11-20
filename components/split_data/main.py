from sklearn.model_selection import train_test_split
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import numpy as np

def split_data(df):
    """Split data to train/test sets
    
    Args
        df : dataframe with the gold data

    Returns
        x_train, x_test : features splitted
        y_train, y_test : target splitted 
    """
    print("Splitting data")

    return train_test_split(
        df.loc[:, df.columns != 'survived'],
        df.survived,
    )


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("--gold_data")
    parser.add_argument("--x_train")
    parser.add_argument("--x_test")
    parser.add_argument("--y_train")
    parser.add_argument("--y_test")

    args = parser.parse_args()

    df = pd.read_csv(args.gold_data)

    # Apply
    X_train, X_test, y_train, y_test = split_data(df)

    # Create file and save content
    Path(args.x_train).parent.mkdir(parents=True, exist_ok=True)
    np.save(args.x_train + '.npy', X_train)
    np.save(args.x_test + '.npy', X_test)
    np.save(args.y_train + '.npy', y_train)
    np.save(args.y_test + '.npy', y_test)
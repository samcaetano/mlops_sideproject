import pandas as pd
import numpy as np
from pathlib import Path
from argparse import ArgumentParser
from sklearn.preprocessing import LabelEncoder

def etl(df : pd.DataFrame):
    """Function to load data and apply transformation to it
    """
    print("ETL dataset")

    # Anonymize data
    f = (df.columns != 'name') \
        & (df.columns != 'home.dest')
    df = df.loc[:, f]

    # Label encode text columns to one_hot
    df.loc[:, 'sex'] = LabelEncoder().fit_transform(df.sex)
    df.loc[:, 'cabin'] = LabelEncoder().fit_transform(df.cabin)
    df.loc[:, 'embarked'] = LabelEncoder().fit_transform(df.embarked)
    df.loc[:, 'ticket'] = LabelEncoder().fit_transform(df.ticket)
    df.loc[:, 'boat'] = LabelEncoder().fit_transform(df.boat)

    # Simple transform
    df = df.fillna(-1)

    # Save gold data
    return df

if __name__ == '__main__':
    parser = ArgumentParser(description='Args for data treatment')
    
    parser.add_argument('--input_filepath')
    parser.add_argument('--output_filepath')

    args = parser.parse_args()

    dataset = pd.read_csv(args.input_filepath)
    
    _dataset = etl(dataset)

        # Save output content
    Path(args.output_filepath).parent.mkdir(parents=True, exist_ok=True)
    _dataset.to_csv(args.output_filepath, index=False)
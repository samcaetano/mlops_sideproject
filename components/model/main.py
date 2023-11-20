import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
import joblib
import json

def training_model(X, y, cv=5):
    """Train the model based on the train/test set of the data.

    Args 
        X : data with features
        y : target
        csv : cross validation steps. Default 5

    Returns
        pipe : fitted LogReg pipeline on the given data samples
        cv_results : json with cv scores in eval time
    """
    print('Training model pipeline')

    # Build pipeline model to be fitted on the data
    pipe = Pipeline(
        [
            ('zscaling', StandardScaler()),
            ('model', LogisticRegression(random_state=0))
        ]
    )

    # Define cross validation step
    cv_results = cross_validate(
        pipe,
        X,
        y,
        cv = cv,
    )

    pipe.fit(X, y)

    return pipe, cv_results

if __name__ == '__main__':
    parser = ArgumentParser(description='Args for model training')
    
    parser.add_argument('--input_filepath')
    parser.add_argument('--input_target_filepath')
    parser.add_argument('--output_model_filepath')
    parser.add_argument('--output_results_filepath')

    args = parser.parse_args()

    # Read gold data to train model
    data = pd.read_csv(args.input_filepath)
    target = pd.read_csv(args.input_target_filepath)

    # Split content in training features and target
    X = data.loc[:, (data.columns != 'survived')]
    y = target

    # Train model pipeline
    model, cv_results = training_model(X, y)

    # Save output content
    Path(args.output_model_filepath).parent.mkdir(parents=True, exist_ok=True) # creates file
    joblib.dump(model, args.output_model_filepath) # save content to created file

    Path(args.output_model_filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_results_filepath, 'w') as f:
        cv_results = json.dumps(
            {k: v.tolist() for k, v in cv_results.items()}
        )
        json.dump(cv_results, f)
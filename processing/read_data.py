import numpy as np
import pandas as pd
from preprocess_df import preprocessing_df

class Person:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


def main():
    df = pd.read_csv('./data/winter_responses_25.csv')
    #print(read_winter.iloc[1,:]) how to access the whole 1st row

    # will have to prompt user for these in reality
    irrev_cols = ["stamp", "mail", "phone", "birthday", "student id", "be able", "link spotify", "gram"]
    # find_name_col()
    preprocessing_df(df, irrev_cols)


if __name__ == "__main__":
    main()
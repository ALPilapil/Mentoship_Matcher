import numpy as np
import pandas as pd
from preprocess_df import preprocessing_df
from partition import partition

def get_similarity_cols(df, target_similarity_cols):
    original_cols = df.columns
    sim_cols = []

    for x in original_cols:
        for target in target_similarity_cols:
            if target in x:
                sim_cols.append(x)

    return sim_cols

def main():
    df = pd.read_csv('./data/winter_responses_25.csv')
    #print(read_winter.iloc[1,:]) how to access the whole 1st row

    # will have to prompt user for these in reality
    irrev_cols = ["stamp", "mail", "phone", "birthday", "student id", "be able", "link spotify", "gram"]
    
    # preprocess the data to remove unnecessary columns and format the text properly
    df = preprocessing_df(df, irrev_cols)

    # define what columns to use semantic similarity on
    target_similarity_cols = ["hobbies", "movies", "genres", "snacks", "hot take", "any other", "describe", "personality traits", "hoping to get", "anyting else"]
    similarity_cols = get_similarity_cols(df, target_similarity_cols)

    # get a list of bigs and a list of littles from the dataframe
    bigs_list, littles_list = partition(df)

    # now compare every big against every little
    # account for edge case of someone being in both categories
    # apply this only to the columns that matter


    # should be a 2 step processs for each person
    # 1. filter for bigs and littles
    # 2. apply semantic similarity on the remaining choices


if __name__ == "__main__":
    main()


#NOTE
# column of rows and littles should be called littles, defined right now as "littos" to match the spreadsheet
import pandas as pd
from preprocess_df import preprocessing_df
from partition import partition
from comparison import get_similarity_cols, run_comparison, score_sort

# test

def main():
    df = pd.read_csv('./data/winter_responses_25.csv')
    #print(read_winter.iloc[1,:]) how to access the whole 1st row

    # will have to prompt user for these in reality
    irrev_cols = ["stamp", "mail", "phone", "birthday", "student id", "be able", "link spotify", "gram"]
    
    # preprocess the data to remove unnecessary columns and format the text properly
    df = preprocessing_df(df, irrev_cols)

    # define what columns to use semantic similarity on, may also have to prompt the user on these
    names_target_cols = ["how comfort", "i wanna", "first, last", "how involved","hobbies/in", "movies", "genres", "snacks", 
                              "hot take", "any other", "describe", "personality traits", "hoping to get", "anything else"]
    target_cols = get_similarity_cols(df, names_target_cols)
    # this contains both columns important for similarity as well as important attributes such as name

    # filter the dataframe to make a copy which contains only the important columns
    target_df = df[target_cols]
    #print(target_df.columns)

    # get a list of bigs and a list of littles from the dataframe
    bigs_list, littles_list = partition(target_df)

    # now compare every big against every little

    # this function should return the top 5 biggest matches along with a breakdown of each score for each category
    comparison_scores = run_comparison(bigs_list, littles_list)
    # sorts the littles for each big in accordance to their average similarity score
    score_sort(comparison_scores) 
    
                          

    for big in comparison_scores:
        print("big: ", big, "\n")
        print("--------------------------------------")


if __name__ == "__main__":
    main()


# TODO: finish the dot product code in comparison.py

# NOTE: 
# column of rows and littles should be called littles, defined right now as "littos" to match the spreadsheet
# remember that we get the column index for role based on the first person and the fact that big, little, or both doesn't appear before the cell which contains
# that person's desired role. 
# - need to make this clear to the user to avoid errors
# attributes no longer contain names or role
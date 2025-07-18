import pandas as pd
from preprocess_df import preprocessing_df
from partition import partition
from comparison import get_similarity_cols, run_comparison, score_sort
import csv

def format_final(comparison_scores, precision, top_N=3, 
                 base_path='base.csv', detailed_path='detailed.csv'):
    """
    comparison_scores: list of [big_name, list_of_littles]
      where each little is [little_name, breakdown, score]
    top_N: how many littles to include per big
    base.csv rows:  big, little1, score1, little2, score2, …
    detailed.csv rows: big, little1, breakdown1, score1, little2, breakdown2, score2, …
    """
    with open(base_path, 'w', newline='', encoding='utf-8') as f_base, \
         open(detailed_path, 'w', newline='', encoding='utf-8') as f_det:

        base_writer = csv.writer(f_base)
        det_writer  = csv.writer(f_det)

        for big, littles in comparison_scores:
            # take only the top_N littles
            top_lits = littles[:top_N]

            # build each row
            base_row = [big]
            det_row  = [big]

            for name, breakdown, score in top_lits:

                rounded_breakdown = [round(v, precision) for v in breakdown]
                rounded_score = round(score, precision)

                base_row.extend([name, rounded_score])
                det_row .extend([name, rounded_breakdown, rounded_score])

            base_writer.writerow(base_row)
            det_writer .writerow(det_row)


def main():
    """
    simply put, takes a csv of the bigs and littles and outputs a csv of those that match best
    inputs:
    - use whole df: a boolean value that is what it sounds like
    - names_target_cols: the names or substrings of the target columns to actually use in the dataset
        - note this only comes into play if use whole df is false
    - weights: the weights by which to calculate scores by
    - top_N: how many top matches do you wanna see per big, if set to 0 show all results
    - precision: what to round all results to

    output:
    - 2 csvs
        - a basic one with names and scores
        - a detailed one with the breakdown
    """

    df = pd.read_csv('./data/winter_responses_25.csv')
    
    # preprocess the data to format the text properly
    df = preprocessing_df(df)

    # define what columns to use semantic similarity on, may also have to prompt the user on these
    names_target_cols = ["how comfort", "i wanna", "first, last", "how involved","hobbies/in", "movies", "genres", "snacks", 
                              "hot take", "any other", "describe", "personality traits", "hoping to get", "anything else"]
    
    # we can probably use this acutally to determine the weights before run time, but still need to ask how much to value each thing
    # it would also be easier to ask here like "please enter substrings of the column names you want to use as well as a score for how much to value them: "
    # would need to ask this regardless of them selecting target cols or not

    target_cols = get_similarity_cols(df, names_target_cols)
    # this contains both columns important for similarity as well as important attributes such as name

    # filter the dataframe to make a copy which contains only the important columns
    target_df = df[target_cols]

    # get a list of bigs and a list of littles from the dataframe
    bigs_list, littles_list = partition(target_df)

    # now compare every big against every little

    # this function should return the top 5 biggest matches along with a breakdown of each score for each category
    comparison_scores = run_comparison(bigs_list, littles_list)

    # sorts the littles for each big in accordance to their total similarity score
    score_sort(comparison_scores) 

    # format into the final csv
    topN = 2                     # user input variable, shows top N littles and the breakdown for each score
    precision = 2                # user input variable for what decimal place to round scores and breakdown to

    format_final(comparison_scores, precision=precision, top_N=topN)


if __name__ == "__main__":
    main()

# NOTE: 
# column of rows and littles should be called littles, defined right now as "littos" to match the spreadsheet
# remember that we get the column index for role based on the first person and the fact that big, little, or both doesn't appear before the cell which contains
# that person's desired role. 
# - need to make this clear to the user to avoid errors
# attributes no longer contain names or role
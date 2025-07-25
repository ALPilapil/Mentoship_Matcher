import pandas as pd
from preprocess_df import preprocessing_df
from partition import partition
from comparison import get_similarity_cols, run_comparison, score_sort, get_weights
import csv 

def format_final(comparison_scores, precision, top_N=3):
    """
    comparison_scores: list of [big_name, list_of_littles]
      where each little is [little_name, breakdown, score]
    precision: number of decimal places to round to
    top_N: how many littles to include per big

    Returns:
      detailed_df: DataFrame with columns
        ['big', 'little1','breakdown1','score1', …]
      base_df:     DataFrame with columns
        ['big', 'little1','score1', …]
    """
    base_rows = []
    detailed_rows = []

    for big, littles in comparison_scores:
        top_lits = littles[:top_N]
        base_row = [big]
        det_row  = [big]

        for name, breakdown, score in top_lits:
            rounded_breakdown = [round(v, precision) for v in breakdown]
            rounded_score     = round(score, precision)

            base_row.extend([name, rounded_score])
            det_row .extend([name, rounded_breakdown, rounded_score])

        base_rows.append(base_row)
        detailed_rows.append(det_row)

    # build column headers
    base_cols = ['big'] + sum(
        [[f'little{i+1}', f'score{i+1}'] for i in range(top_N)], []
    )
    det_cols = ['big'] + sum(
        [[f'little{i+1}', f'breakdown{i+1}', f'score{i+1}'] for i in range(top_N)], []
    )

    base_df     = pd.DataFrame(base_rows, columns=base_cols)
    detailed_df = pd.DataFrame(detailed_rows, columns=det_cols)

    return detailed_df, base_df


def main(input_df, name_col_label, role_col_label, topN, precision, weights):
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
    
    # preprocess the data to format the text properly
    df = preprocessing_df(input_df)

    # define what columns to use semantic similarity on, may also have to prompt the user on these
    names_target_cols = df.columns
    
    # we can probably use this acutally to determine the weights before run time, but still need to ask how much to value each thing
    # it would also be easier to ask here like "please enter substrings of the column names you want to use as well as a score for how much to value them: "
    # would need to ask this regardless of them selecting target cols or not

    target_cols = get_similarity_cols(df, names_target_cols)
    # this contains both columns important for similarity as well as name

    # filter the dataframe to make a copy which contains only the important columns
    target_df = df[target_cols]

    # get the weights here in main 
    print("The bigger the value to each corresponding attribute the more it the algorithm will value it")

    
    # get a list of bigs and a list of littles from the dataframe
    bigs_list, littles_list = partition(target_df)

    # now compare every big against every little
    # this function should return the top 5 biggest matches along with a breakdown of each score for each category
    comparison_scores = run_comparison(bigs_list, littles_list, weights)

    # sorts the littles for each big in accordance to their total similarity score
    score_sort(comparison_scores) 

    # format into the final csv
    detailed_df, base_df = format_final(comparison_scores, precision=precision, top_N=topN)

    print(detailed_df)
    print("------------------------")
    print(base_df)


if __name__ == "__main__":
    # these are known by the user before hand
    input_df = pd.read_csv('./data/trimed_winter_responses_25.csv')
    name_col_label = "name (first, last)"
    role_col_label = "I wanna be a..."
    topN = 3
    precision = 3

    # need to exclude names and the role from the list of weights
    cols_no_names_roles = input_df.columns.tolist()
    cols_no_names_roles.remove(name_col_label)
    cols_no_names_roles.remove(role_col_label)
    weights = get_weights(cols_no_names_roles)

    main(input_df, name_col_label, role_col_label, topN, precision, weights)

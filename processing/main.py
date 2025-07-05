import numpy as np
import pandas as pd
from preprocess_df import preprocessing_df
from partition import partition
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')


# comparison

def get_similarity_cols(df, target_similarity_cols):
    original_cols = df.columns
    sim_cols = []

    for x in original_cols:
        for target in target_similarity_cols:
            if target in x:
                sim_cols.append(x)

    return sim_cols

def encode_attributes(text_attributes):
    encoded_att = []
    for x in text_attributes:
        text = str(x)      # converts the int to a string
        vec_att = model.encode([text])[0]
        encoded_att.append(vec_att)

    return encoded_att

def get_similarities(encoded_one, encoded_two):
    similarity_list = []

    for x,y in zip(encoded_one, encoded_two):
        similarity_score = 1-distance.cosine(x,y)
        similarity_list.append(similarity_score)

    return similarity_list


def run_comparison(bigs_list, littles_list):
    # temporary, reduce the list size just for ease and faster run time
    bigs_list = bigs_list[:2]
    littles_list = littles_list[:3]

    # for each big
    #   encode each attribute 
    #   get a little
    #       run semantic similarity on the ith attribute of the big and the ith attribute of the little
    #       save the ith score on the ith position in a list 
    #       save the ith attribute which this is for, for interpretability. just do this as literally its index for now
    #   get the next little

    matched_tuples = []

    for big in bigs_list:
        big_encoded = encode_attributes(big.attributes)
        # a list to keep track of all the littles and their scores
        little_tuples = []

        for little in littles_list:
            little_encoded = encode_attributes(little.attributes)
            # run similarity on the ith of the big and the ith of the little
            sim_scores = get_similarities(big_encoded, little_encoded)
            abs_sim_scores = list(map(abs, sim_scores))
            total_score = np.array(abs_sim_scores).mean()                   # toy with this to get different results, mean, sum, etc. 
            name_score_tuple = (little.name, abs_sim_scores, total_score)   # every tuple contains the name and a list of the sim scores
            little_tuples.append(name_score_tuple)

        # now you have a list of tuples, need to assign this list to the big via another tuple
        big_tuple = (big.name, little_tuples)
        matched_tuples.append(big_tuple)

    # matched tuples is a big list
    # - each element is a big and all the littles
    #   - each one of these elements is a tuple, the first element is that littles name and the second is a list of the corresponding scores

    return matched_tuples


# organize the results from above based on total score
def score_sort(matched_tuples):
    for big in matched_tuples:
        # sort the list of littles according to their total score
        sorted(matched_tuples[1], key=lambda little: little[3])

    
    # print tests
    print("big name along with little info: ", matched_tuples[0], "\n")
    print("first big name: ", matched_tuples[0][0], "\n")
    print("second big name: ", matched_tuples[1][0], "\n")
    print("little info for the first big: ", matched_tuples[0][1], "\n")
    print("first little of the first big: ", matched_tuples[0][1][0], "\n")
    print("second little of the first big: ", matched_tuples[0][1][1], "\n")
    print("name of the first little of the first big: ", matched_tuples[0][1][0][0], "\n")
    print("total score of the first little of the first big: ", matched_tuples[0][1][0][2], "\n")


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

    # now compare every big against every little or vice versa
    # account for edge case of someone being in both categories
    # apply this only to the columns that matter

    # this function should return the top 5 biggest matches along with a breakdown of each score for each category
    comparison_scores = run_comparison(bigs_list, littles_list)

    sorted_matches = score_sort(comparison_scores)

    # should be a 2 step processs for each person
    # 1. filter for bigs and littles
    # 2. apply semantic similarity on the remaining choices


if __name__ == "__main__":
    main()


#NOTE
# column of rows and littles should be called littles, defined right now as "littos" to match the spreadsheet
# remember that we get the column index for role based on the first person and the fact that big, little, or both doesn't appear before the cell which contains
# that person's desired role. 
# - need to make this clear to the user to avoid errors
# attributes no longer contain names or role
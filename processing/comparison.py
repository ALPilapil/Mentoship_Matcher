# comparison
import numpy as np
from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')


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

def calculate_total_score(sim_array):
    # need to get the length of the array of total scores
    # then make a list of weights of equal weights
    # then prompt the user for values for these weights
    # get a dot product (weights, scores)

    return 

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
        # print("before: -------------------------\n")
        # print(big)
        big[1].sort(key=lambda t: t[2], reverse=True)
        # print("after: --------------------------\n")
        # print(big)
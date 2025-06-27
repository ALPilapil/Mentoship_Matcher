# testing out the basics of semantic matching
# use BERT since it's the most common

#!pip install -U sentence-transformers

from scipy.spatial import distance
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample sentence
# sentences = ["The movie is awesome. It was a good thriller",
#              "We are learning NLP throughg GeeksforGeeks",
#              "The baby learned to walk in the 5th month itself"]

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# test = "I liked the movie."
# print('Test sentence:',test)
# test_vec = model.encode([test])[0]

test = "5"
test_vec = model.encode([test])[0]


for sent in numbers:
    similarity_score = 1-distance.cosine(test_vec, model.encode([sent])[0])
    print(f'\nFor {sent}\nSimilarity Score = {similarity_score} ')


# SEMANTIC SIMILARITY APPLIES TO NUMBERS, 5=5, 5 close to 6 and 4, far from 10 and 1
import glob
import numpy as np
import scipy as sp
from random import random


file_names = glob.glob('*.txt')

def getNews(file_name, delim='\n'):
    with open(file_name, 'r') as file:
        return file.read().split(delim)

news = []
for file_name in file_names:
    news += getNews(file_name)
news = [news.replace('\n', '') for news in news]

corpus = ""
for file_name in file_names:
    with open(file_name, 'r') as file:
        corpus += file.read()
corpus = corpus.replace('\n',' ')
corpus = corpus.replace('\t',' ')
corpus = corpus.replace('“', ' " ')
corpus = corpus.replace('”', ' " ')
corpus = corpus.replace('„', ' " ')
for spaced in ['.',',','!','?','(','—',')','"']:
    corpus = corpus.replace(spaced, ' {0} '.format(spaced))
corpus_words = corpus.split(' ')
corpus_words = [word for word in corpus_words if word != '']

distinct_words = list(set(corpus_words))
word_idx_dict = {word: i for i, word in enumerate(distinct_words)}
distinct_words_count = len(distinct_words)

k = 2
sets_of_k_words = [' '.join(corpus_words[i:i+k]) for i, _ in enumerate(corpus_words[:-k])]

from scipy.sparse import dok_matrix
distinct_sets_of_k_words = list(set(sets_of_k_words))
sets_count = len(distinct_sets_of_k_words)
next_after_k_words_matrix = dok_matrix((sets_count, distinct_words_count))

k_words_idx_dict = {word: i for i, word in enumerate(distinct_sets_of_k_words)}

for i, word in enumerate(sets_of_k_words[:-k]):
    word_sequence_idx = k_words_idx_dict[word]
    next_word_idx = word_idx_dict[corpus_words[i+k]]
    next_after_k_words_matrix[word_sequence_idx, next_word_idx] +=1

def weighted_choice(objects, weights):
    """ returns randomly an element from the sequence of 'objects', 
        the likelihood of the objects is weighted according 
        to the sequence of 'weights', i.e. percentages."""

    weights = np.array(weights, dtype=np.float64)
    sum_of_weights = weights.sum()
    # standardization:
    np.multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]

def sample_next_word_after_sequence(word_sequence, alpha = 0):
    next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence]] + alpha
    likelihoods = next_word_vector/next_word_vector.sum()
    return weighted_choice(distinct_words, likelihoods.toarray())

def stochastic_chain(seed, chain_length=15):
    current_words = seed.split(' ')
    sentence = seed

    for _ in range(chain_length):
        sentence+=' '
        next_word = sample_next_word_after_sequence(' '.join(current_words))
        sentence+=next_word
        current_words = current_words[1:]+[next_word]
    return sentence

print(stochastic_chain('Рекорден брой'))
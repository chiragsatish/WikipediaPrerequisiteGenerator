import numpy as np
import re
from operator import itemgetter
np.seterr(divide='ignore', invalid='ignore')

# Cosine Similarity = cos(theta) = (A . B) / (||A|| ||B||)
def cosineSimilarity(vector1, vector2):
    dotProduct = np.dot(vector1, vector2)
    normV1 = np.linalg.norm(vector1)
    normV2 = np.linalg.norm(vector2)
    return dotProduct / (normV1 * normV2)

# A function to calculate the similarity between two sentences
def sentenceSimilarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []

    # Reduce all words to lower case
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]
    # Put all words into a set, so that only one occurance is present
    allWords = list(set(sentence1 + sentence2))
 
    vector1 = [0] * len(allWords)
    vector2 = [0] * len(allWords)
 
    # build the vector for the first sentence
    # Vector is nothing but setting the index of the word
    # For example, if sentence1 is 'My name is Avinash'
    # And sentence2 is 'I like Chocolates'
    # Vector1 = [1,1,1,1,0,0,0], Vector2 = [0,0,0,0,1,1,1] 
    # where 1s correspond to the words present
    for word in sentence1:
        if word in stopwords:
            continue
        vector1[allWords.index(word)] += 1
 
    # build the vector for the second sentence
    for word in sentence2:
        if word in stopwords:
            continue
        vector2[allWords.index(word)] += 1
 
    return cosineSimilarity(vector1, vector2)

# A function to clean the text of whitespaces
# Returns list of lists
def processText(text):
    try:
        text = re.sub('[\n\t +]', ' ', text)
    except:
        pass
    sentenceList = list()
    wordList = list()
    tempList = text.strip().split(".")
    for sentence in tempList:
        wordList = sentence.strip().split(" ")
        if len(wordList) > 1:
            sentenceList.append(wordList)
    return sentenceList, len(sentenceList)
 
 # A function to compute the similarity matrix
def buildSimilarityMatrix(sentences, stopwords=None):
    # Create an empty similarity matrix
    S = np.zeros((len(sentences), len(sentences)))

    for index1 in range(len(sentences)):
        for index2 in range(len(sentences)):
            # To eliminate calculating similarity of same sentences
            if index1 == index2:
                continue
            # If sentences are not same calculate the similarity
            S[index1][index2] = sentenceSimilarity(sentences[index1], sentences[index2], stopwords)
 
    # normalize the matrix row-wise
    for index in range(len(S)):
        if S[index].sum() > 0:
            S[index] /= S[index].sum()
        else:
            S[index] = 1
 
    return S

# Function to rank the sentences using textrank algo
# Stop the algorithm when the difference between 2 consecutive iterations is smaller or equal to eps
# With a probability of 1-d, simply pick a sentence at random as the next valid sentence
def ranking(A, eps=0.0001, d=0.85):
    P = np.ones(len(A)) / len(A)
    while True:
        newP = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs((newP - P).sum())
        if delta <= eps:
            return newP
        if not np.isfinite(newP).all():
        	return newP
        P = newP

# Function to calculate the ranks of the most important sentences in the text
def textrank(sentences, linesinSummary=5, stopwords=None):
    S = buildSimilarityMatrix(sentences, stopwords) 
    sentenceRanks = ranking(S)
 
    # Sort the sentence ranks
    rankedSentenceIndexes = [item[0] for item in sorted(enumerate(sentenceRanks), key=lambda item: -item[1])]
    selectedSentences = sorted(rankedSentenceIndexes[:linesinSummary])
    summary = itemgetter(*selectedSentences)(sentences)
    return summary

# Main function for the code
def textRankDriver(text):
    sentences, length = processText(text)    
    S = buildSimilarityMatrix(sentences)    
    # Create summary
    summary = ""
    for wordList in textrank(sentences):
        sentence = ' '.join(wordList)
        sentence += '. '
        summary += sentence
    return summary
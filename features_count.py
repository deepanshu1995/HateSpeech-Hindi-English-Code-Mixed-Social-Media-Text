#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import nltk
from preprocessing import *
from format_data import *

global n_char_gram, n_word_gram
n_char_gram = 3
n_word_gram = 3

char_n_grams_index = {}
word_n_grams_index = {}
hate_words_index = {}

def GetAllCharNGrams(tweet_mapping):
	char_n_grams = []
	for key, tweet in tweet_mapping.iteritems():
		char_grams = CharNGrams(tweet, n_char_gram)
		char_n_grams.extend(char_grams)

		char_n_grams = set(char_n_grams)
		char_n_grams = list(char_n_grams)
	return char_n_grams

def GetAllWordNGrams(tweet_mapping):
	word_n_grams = []
	for key, tweet in tweet_mapping.iteritems():
		tokenised_tweet = TokeniseTweet(tweet)
		#print tokenised_tweet
		word_grams = WordNGrams(tokenised_tweet, n_word_gram)
		word_n_grams.extend(word_grams)

		word_n_grams = set(word_n_grams)
		word_n_grams = list(word_n_grams)
	return word_n_grams


def CharNGramIndex(char_n_grams):
	count = 0
	for char_gram in char_n_grams:
		char_n_grams_index[char_gram] = count
		count = count + 1

def WordNGramsIndex(word_n_grams):
	count = 0
	for word_gram in word_n_grams:
		word_n_grams_index[word_gram] = count
		count = count + 1

def HateWordsIndex(hate_words):
	count = 0
	for hate_word in hate_words:
		hate_words_index[hate_word] = count
		count = count + 1

def ProcessTweetforWordNGrams(tweet_mapping):
	processed_tweet_mapping = {}
	for key, tweet in tweet_mapping.iteritems():
		tokenised_tweet = TokeniseTweet(tweet)
		processed_tweet = ProcessTweet(tokenised_tweet)
		delimiter = ' '
		processed_tweet = delimiter.join(processed_tweet)
		processed_tweet = RemovePunctuations(processed_tweet)
		processed_tweet_tokenised = TokeniseTweet(processed_tweet)
		processed_tweet = delimiter.join(processed_tweet_tokenised)

		processed_tweet_mapping[key] = processed_tweet

	return processed_tweet_mapping

def HateWords(file):
	hate_words = []
	for line in file:
		hate_words.append(line.strip())

	return hate_words

def CreatePickleFile():
	file = open('hate_lexicon.txt', 'r')
	hate_words = HateWords(file)
	hate_words = set(hate_words)
	hate_words = list(hate_words)
	hate_words = sorted(hate_words)
	#print len(hate_words)
	#print hate_words
	HateWordsIndex(hate_words)
	#print hate_words_index
	id_to_tweet_map = create_id_tweet_map()
	#print id_to_tweet_map
	char_n_grams = GetAllCharNGrams(id_to_tweet_map)
	#print char_n_grams
	processed_tweet_map = ProcessTweetforWordNGrams(id_to_tweet_map)
	#print processed_tweet_map
	word_n_grams = GetAllWordNGrams(processed_tweet_map)

	#print word_n_grams
	CharNGramIndex(char_n_grams)
	#print char_n_grams_index
	WordNGramsIndex(word_n_grams)
	#print word_n_grams_index
	pickle_data_file = open('pickle_data.txt', "wb")

	# Here 3 is the number which tells how many python objects are getting
	# dumped into pickle file. This argument can be used to use do a range
	# based traversal into a pickle file.
	pickle.dump(3, pickle_data_file)
	pickle.dump(char_n_grams_index, pickle_data_file)
	pickle.dump(word_n_grams_index, pickle_data_file)
	pickle.dump(hate_words_index, pickle_data_file)
	pickle_data_file.close()
CreatePickleFile()

#print len(hate_words_index)
#print hate_words_index['virodh']

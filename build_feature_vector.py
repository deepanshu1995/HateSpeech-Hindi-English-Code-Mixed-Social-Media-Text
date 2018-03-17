#! #!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer
import numpy as np
import operator
import pickle
import preprocessing as pre
import re
import string
global char_n_grams_index, word_n_grams_index, hate_words_index

def AddEmoticonFeatures(feature_vector, happy_emoticon, sad_emoticon,
						disgust_emoticon, anger_emoticon, fear_emoticon,
						surprise_emoticon):
	count_happy = count_sad = count_disgust = count_anger = count_fear = count_surprise = 0
	#print "AddEmoticonFeatures Called"
	for emoticon in pre.all_emoticons:
		if emoticon in happy_emoticon:
			count_happy = count_happy + 1
		elif emoticon in sad_emoticon:
			count_sad = count_sad + 1
		elif emoticon in anger_emoticon:
			count_anger = count_anger + 1
		'''
		elif emoticon in disgust_emoticon:
			count_disgust = count_disgust + 1
		
		elif emoticon in fear_emoticon:
			count_fear = count_fear + 1
		elif emoticon in surprise_emoticon:
			count_surprise = count_surprise + 1
		'''
	feature_vector.append(count_happy)
	feature_vector.append(count_sad)
	#feature_vector.append(count_disgust)
	feature_vector.append(count_anger)
	#feature_vector.append(count_fear)
	#feature_vector.append(count_surprise)

	return feature_vector

def AddCharNGramFeatures(feature_vector, char_n_grams_index, char_n_grams):
	char_features = [0]*len(char_n_grams_index)
	#print "AddCharNGramFeatures Called"
	for char_gram in char_n_grams:
		if char_gram in char_n_grams_index:
			char_features[char_n_grams_index[char_gram]] = 1
	feature_vector.extend(char_features)
	return feature_vector

def AddWordNGramFeatures(feature_vector, word_n_grams_index, word_n_grams):
	word_features = [0]*len(word_n_grams_index)
	#print "AddWordNGramFeatures Called"
	for word_gram in word_n_grams:
		if word_gram in word_n_grams_index:
			word_features[word_n_grams_index[word_gram]] = 1
	feature_vector.extend(word_features)
	return feature_vector

def AddHateWordsFeature(feature_vector, hate_words_index, tweet_hate_words):
	hate_feature = [0]*len(hate_words_index)
	#print len(hate_feature)
	for hate_word in tweet_hate_words:
		if hate_word in hate_words_index:
			#print hate_word
			hate_feature[hate_words_index[hate_word]] = 1
			#print hate_words_index[hate_word]
	feature_vector.extend(hate_feature)
	return feature_vector

def AddPunctuationMarksFeature(feature_vector, punctuations_marks_count):
	for punctuation in pre.punctuations_marks:
		if punctuation in punctuations_marks_count:
			feature_vector.append(1)
		else:
			feature_vector.append(0)
	feature_vector.append(len(punctuations_marks_count))

	return feature_vector

def AddRepetitiveWordsFeature(feature_vector, repetitive_words):
	#print "AddRepetitiveWordsFeature Called"
	if len(repetitive_words) > 0:
		feature_vector.append(1)
	else:
		feature_vector.append(0)
	#feature_vector.append(len(repetitive_words))

	return feature_vector

def AddUpperCaseWordsFeature(feature_vector, upper_case_words):
	if len(upper_case_words) > 0:
		feature_vector.append(1)
	else:
		feature_vector.append(0)
	#feature_vector.append(len(upper_case_words))

	return feature_vector

def AddIntensifersFeature(feature_vector, intensifiers):
	if len(intensifiers) > 0:
		feature_vector.append(1)
	else:
		feature_vector.append(0)
	#feature_vector.append(len(intensifiers))

	return feature_vector

def AddNegationsFeature(feature_vector, negations):
	if len(negations) > 0:
		feature_vector.append(1)
	else:
		feature_vector.append(0)
	#feature_vector.append(len(negations))
	return feature_vector


def BuildFeatureVectorForTweet(tweet):

	#print "BuildFeatureVectorForTweet Called"
	global char_n_grams_index, word_n_grams_index, hate_words_index
	happy, sad, anger, fear, surprise, disgust, hashtags, usernames, \
	urls, punctuations_marks_count, repetitive_words, char_n_grams, \
	word_n_grams, upper_case_words, intensifiers, negations, tweet_hate_words = pre.PreProcessing(tweet)	
	#print tweet_hate_words
	feature_vector = []
	#print char_n_grams_index
	#print word_n_grams_index
	#feature_vector = AddEmoticonFeatures(feature_vector, happy, sad, disgust, anger, fear, surprise)
	feature_vector = AddCharNGramFeatures(feature_vector, char_n_grams_index, char_n_grams)
	#feature_vector = AddWordNGramFeatures(feature_vector, word_n_grams_index, word_n_grams)
	#feature_vector = AddRepetitiveWordsFeature(feature_vector, repetitive_words)
	#feature_vector = AddPunctuationMarksFeature(feature_vector, punctuations_marks_count)
	#feature_vector = AddHateWordsFeature(feature_vector, hate_words_index, tweet_hate_words)
	#feature_vector = AddUpperCaseWordsFeature(feature_vector, upper_case_words)
	#feature_vector = AddIntensifersFeature(feature_vector, intensifiers)
	#feature_vector = AddNegationsFeature(feature_vector, negations)
	return feature_vector



def GetFeatureVector(tweet):
	#print "GetFeatureVector Called"
	global char_n_grams_index, word_n_grams_index, hate_words_index
	file = open('pickle_data.txt', "rb")
	data = []
	# If file reaches the EOL while reading this will reset and the reading
	# will start from beginning
	file.seek(0)

	for i in xrange(pickle.load(file)):
		data.append(pickle.load(file))

	char_n_grams_index, word_n_grams_index, hate_words_index = data

	file.close()

	feature_vector = BuildFeatureVectorForTweet(tweet)
	return feature_vector


def FeatureVectorDictionary(tweet_mapping):
	feature_vector_dict = {}
	for key, tweet in tweet_mapping.iteritems():
		feature_vector_dict[key] = GetFeatureVector(tweet)
	return feature_vector_dict


def TrainingData(id_tweet_map, id_class_map):
	tweet_feature_vector = []
	tweet_class = []
	#print "TrainingData Called"
	#print "FeatureVectorDictionary Called"
	feature_vector_dict = FeatureVectorDictionary(id_tweet_map)
	#print "Done"
	for key, val in feature_vector_dict.iteritems():
		tweet_feature_vector.append(feature_vector_dict[key])
		tweet_class.append(id_class_map[key])

	return tweet_feature_vector, tweet_class

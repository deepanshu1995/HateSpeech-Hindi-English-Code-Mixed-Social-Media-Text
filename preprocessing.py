#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import re
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import PorterStemmer

snowball_stemmer = SnowballStemmer('english')
porter_stemmer = PorterStemmer()
# Emoticons for different classes
happy_emoticons = \
	[':)',';)', '=)', ':]', ':P', ':-P', ';P', \
	':D', ';D', ':>', ':3', ':-)', ';-)', ':^)', \
	':o)', ':~)', ';^)', ';o)', '-D', ':->', ':\')',\
	]

sad_emoticons = \
	[':(', '=(', ':-(', ':^(',\
	 ':o(', ':^(', ':\'(', ':-<', \
	]

anger_emoticons = \
	['>:S', '>:{', '>:', 'x-@', \
	 ':@', ':-@', ':-/', ':-\\', ':/', \
	]
surprised_emoticons = \
	[':-o', ':-O', 'o_O', 'O_o', ':$', \
	]

fear_emoticons = \
	['D:', ':!', \
		]

disgust_emoticons = \
	['DX', \
	]

all_emoticons = []
all_emoticons.extend(happy_emoticons)
all_emoticons.extend(sad_emoticons)
all_emoticons.extend(anger_emoticons)
all_emoticons.extend(surprised_emoticons)
all_emoticons.extend(fear_emoticons)
all_emoticons.extend(disgust_emoticons)

all_intensifiers = \
	['amazingly', 'astoundingly', 'awful', 'bare', 'bloody', \
	 'crazy', 'dead', 'dreadfully', 'colossally', 'especially', 'exceptionally', \
	 'excessively', 'extremely', 'extraordinarly', 'fantastically', 'frightfully', \
	 'fucking', 'fully', 'hella', 'holy', 'incredibly', 'insanely', 'literally', \
	 'mad', 'mightily', 'moderately', 'most', 'outrageously', 'phenomenally', \
	 'precious', 'quite', 'radically', 'rather', 'real', 'really', 'remarkably', \
	 'right', 'sick', 'so,', 'somewhat', 'strikingly', 'super', 'supremely', 'surpassingly', \
	 'terribly', 'terrifically', 'too', 'totally', 'uncommonly', 'unusually', 'veritable', 'very', \
	 'wicked'
	]

negations_words = \
	['never', 'no', 'nothing', 'nowhere', 'noone', 'none', 'not', 'haven\'t', \
	 'hasn\'t', 'hadn\'t', 'can\'t', 'couldn\'t', 'shouldn\'t', 'won\'t', 'wouldn\'t', \
	 'don\'t', 'doesn\'t', 'didn\'t', 'isn\'t', 'aren\'t', 'ain\'t', 'n\'t'
	]
punctuations_marks = string.punctuation
punctuations_marks = punctuations_marks + '¿'


# Takes tokenised tweet as input argument and return the list of emoticons
# present in the tweet.
def GetEmoticons(tweet):
	happy = []
	sad = []
	anger = []
	surprise = []
	fear = []
	disgust = []

	for emoticon in happy_emoticons:
		if emoticon in tweet:
			happy.append(emoticon)

	for emoticon in sad_emoticons:
		if emoticon in tweet:
			sad.append(emoticon)

	for emoticon in anger_emoticons:
		if emoticon in tweet:
			anger.append(emoticon)

	for emoticon in surprised_emoticons:
		if emoticon in tweet:
			surprise.append(emoticon)

	for emoticon in fear_emoticons:
		if emoticon in tweet:
			fear.append(emoticon)

	for emoticon in disgust_emoticons:
		if emoticon in tweet:
			disgust.append(emoticon)


	return happy, sad, anger, surprise, fear, disgust

# Takes tokenised tweet as input argument and return the list of hash tags
# present in the tweet.
def GetHashTags(tweet):
	hashtags = []
	for token in tweet:
		if token[0]=='#':
			hashtags.append(token.lower())

	return hashtags

# Takes tokenised tweet as input argument and return the list of negation words
# present in the tweet:
def FindAllNegations(tweet):
	negations = []
	for word in negations_words:
		if word in tweet:
			negations.append(word)
	return negations

# Takes tokenised tweet as input argument and return the list of intensifiers
# present in the tweet.
def GetIntensifiers(tweet):
	intensifiers = []
	for intensifier in all_intensifiers:
		if intensifier in tweet:
			intensifiers.append(intensifier)
	return intensifiers

# Takes tokenised tweet as input argument and return the list of usernames
# present in the tweet.
def GetUserNames(tweet):
	user_names = []
	for token in tweet:
		if token[0]=='@':
			user_names.append(token)
	return user_names

# Takes tweet as input argument and return the list of URL's present
# in the tweet.
def GetURLs(tweet):
	url_regex = [r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+']
	url_re = re.compile(r'('+'|'.join(url_regex)+')', re.VERBOSE | re.IGNORECASE)
	urls = url_re.findall(tweet)
	return urls

# Remove punctuation marks from a preprocessed tweet.
def RemovePunctuations(processed_tweet):
	processed_tweet = processed_tweet.translate(None, punctuations_marks)
	return processed_tweet

# Find the score using the emotion lexicon
def FindLexiconScore(tokenised_tweet, id_to_word_map, id_to_score_map):
	score_vector = [0]*len(id_to_word_map)
	for key, word in id_to_word_map.iteritems():
		if word in tokenised_tweet:
			score_vector[key] = id_to_score_map[key]

	return score_vector

# Get Count of all punctuation marks from a preprocessed tweet.
def GetPunctuationMarks(processed_tweet):
	punctuations_marks_count = {}
	for char in processed_tweet:
		if char in punctuations_marks:
			if char in punctuations_marks_count:
				punctuations_marks_count[char]+=1
			else:
				punctuations_marks_count[char]=1
	return punctuations_marks_count

'''
Takes tokenised tweet as input argument and process it by replacing all the
usernames with 'USER', URLs with "URL" and HashTags with "HASHTAG", emoticons
with "EMOTICONS." We are not converting the tweet to lowercase.
'''
def ProcessTweet(tweet):
	processed_tweet = tweet
	for i in xrange(len(processed_tweet)):
		if processed_tweet[i][0] == '@':
			processed_tweet[i] = 'USER'
		elif processed_tweet[i][0] == '#':
			processed_tweet[i] = 'HASHTAG'
		elif 'http' in processed_tweet[i]:
			processed_tweet[i] = 'URL'
		elif processed_tweet[i] in happy_emoticons:
			processed_tweet[i] = 'EMOTICON'
		elif processed_tweet[i] in sad_emoticons:
			processed_tweet[i] = 'EMOTICON'
		elif processed_tweet[i] in anger_emoticons:
			processed_tweet[i] = 'EMOTICON'
		elif processed_tweet[i] in fear_emoticons:
			processed_tweet[i] = 'EMOTICON'
		elif processed_tweet[i] in surprised_emoticons:
			processed_tweet[i] = 'EMOTICON'
		elif processed_tweet[i] in disgust_emoticons:
			processed_tweet[i] = 'EMOTICON'
	return processed_tweet

# Split the tweet into tokens.
def TokeniseTweet(tweet):
	tokenised_tweet = tweet.split(' ')
	tokenised_tweet = filter(None, tokenised_tweet)
	return tokenised_tweet

# Generate the Skip Grams for the tweet. Input argument is the tokenised
# tweet,n is the number of grams. If n =1 unigrams, n=2 bigrams and so on.
'''
def WordNGrams(tweet, n):
	word_ngrams_list = []
	#print tweet
	for num in range(0, len(tweet)+1-n):
		wordngrams = ' '.join(tweet[num:num+n])
		word_ngrams_list.append(wordngrams)
	return word_ngrams_list
'''
def WordNGrams(tweet, n):
	word_n_grams_list = []
	for i in xrange(1, n + 1):
		word_i_grams = [" ".join(tweet[j:j+i]) for j in xrange(len(tweet) - (i-1))]
		word_n_grams_list.extend(word_i_grams)
	return word_n_grams_list


# Generate the charngrams for a tweet. Input is the tweet not the tokenised
# one, n is the number of grams.
'''
def CharNGrams(tweet, n):
	char_ngrams_list = []
	for num in range(0, len(tweet)-n+1):
		charngrams = tweet[num:num+n]
		char_ngrams_list.append(charngrams)
	return char_ngrams_list
'''
def CharNGrams(tweet, n):
	char_n_grams_list = []
	for i in xrange(1, n + 1):
		char_i_grams = [tweet[j:j+i] for j in xrange(len(tweet)- (i-1))]
		char_n_grams_list.extend(char_i_grams)
	return char_n_grams_list

def TweetHateWords(tweet, all_hate_words):
	hate_words = []
	for token in tweet:
		if token in all_hate_words:
			hate_words.append(token)
	return hate_words

def ReplaceTwoOrMore(word):
	#print word
	#pattern = re.compile(r"(.)\1{1}", re.DOTALL)
	#return pattern.sub(r"\1\1", word)
	return re.sub(r'(.)\1+', r'\1\1', word)

def CheckRepetitions(tweet):
	repetitive_words = []
	processed_tweet = tweet
	#print processed_tweet
	for i in xrange(len(processed_tweet)):
		word = processed_tweet[i]
		#print word
		#print ReplaceTwoOrMore(word)
		if processed_tweet[i] != ReplaceTwoOrMore(word):
			repetitive_words.append(processed_tweet[i])
			processed_tweet[i] = ReplaceTwoOrMore(word)
	return repetitive_words


def FindUpperCaseWords(tweet):

	re_pattern = r'\b[A-Z]{4,}\b'
	upper_case_words = re.findall(re_pattern, tweet)
	return upper_case_words

def HateWords(file):
	hate_words = []
	for line in file:
		hate_words.append(line.strip())

	return hate_words

def PreProcessing(tweet):
	file = open('hate_lexicon.txt', 'r')
	tokenised_tweet = TokeniseTweet(tweet)
	#print tokenised_tweet
	happy, sad, anger, fear, surprise, disgust = GetEmoticons(tokenised_tweet)
	hashtags = GetHashTags(tokenised_tweet)
	intensifiers = GetIntensifiers(tokenised_tweet)
	negations = FindAllNegations(tokenised_tweet)

	all_hate_words = HateWords(file)
	all_hate_words = sorted(all_hate_words)
	file.close()
	#print all_hate_words
	tweet_hate_words = TweetHateWords(tokenised_tweet, all_hate_words)
	usernames = GetUserNames(tokenised_tweet)
	#score_vector = FindLexiconScore(tokenised_tweet, create_id_word_map(), create_id_to_score_map())
	urls = GetURLs(tweet)
	upper_case_words = FindUpperCaseWords(tweet)
	processed_tweet = ProcessTweet(tokenised_tweet)
	
	delimiter = ' '
	processed_tweet = delimiter.join(processed_tweet)
	
	punctuations_marks_count = GetPunctuationMarks(processed_tweet)
	processed_tweet = RemovePunctuations(processed_tweet)
	processed_tweet_tokenised = TokeniseTweet(processed_tweet)
	processed_tweet = delimiter.join(processed_tweet_tokenised)

	repetitive_words = CheckRepetitions(processed_tweet_tokenised)
	char_n_grams = CharNGrams(processed_tweet,3)
	word_n_grams = WordNGrams(processed_tweet_tokenised, 3)

	return happy, sad, anger, fear, surprise, disgust, hashtags, usernames, \
		   urls, punctuations_marks_count, repetitive_words, char_n_grams, \
		   word_n_grams, upper_case_words, intensifiers, negations, tweet_hate_words


#tweet = "Heyyyyy I am verrryyy happppyyyy nafrat murder"
#test = PreProcessing(tweet)
#print test
#print word
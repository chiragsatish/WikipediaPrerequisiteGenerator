from function import linkify, getLinks, extractKeywordsUsingRake, extractTextData, filterCat, Compare,keyword_filtering,keyword_filtering_category
from extractive import textRankDriver # Import functions for summarization from extractive.py 
import wikipediaapi
import wikipedia
import time
import sys
import socket
import urllib.error

def basicSearch(subject):
	pageLink = linkify(subject)
	try:
		linkList = getLinks(pageLink)
	except urllib.error.HTTPError as err:
		if err.code == 404:
			return ("Check the input.", "")
	except socket.error:
		return ("Check the internet connection.", "")

	summ = wikipedia.summary(subject,sentences = 4)
	dataList = extractKeywordsUsingRake(subject) 
	keywordSet_temp = keyword_filtering(dataList,linkList)
	keywordSet = keyword_filtering_category(subject, keywordSet_temp)
	keywordSet = [x for x in keywordSet if x != subject]
	if len(keywordSet) < 3:
		return (str(len(keywordSet))+" keywords in subject. Try advanced search.", "")

	for each in keywordSet:
		if each != subject:
			text = extractTextData(each)
			summ += "\n\n"+each+":\n"
			summ += textRankDriver(text)

	return (subject, summ)

def advancedSearch(subject):
	pageLink = linkify(subject)
	try:
		linkList = getLinks(pageLink)
	except urllib.error.HTTPError as err:
		if err.code == 404:
			return ("Check the input.", "")
	except socket.error:
		return ("Check the internet connection.", "")

	summ = wikipedia.summary(subject,sentences = 4)
	dataList = extractKeywordsUsingRake(subject, 1, 4, 1)
	keywordSet_temp = keyword_filtering(dataList,linkList)
	keywordSet = keyword_filtering_category(subject, keywordSet_temp)
	keywordSet = [x for x in keywordSet if x != subject]
	if len(keywordSet) < 5:
		keywordSet = linkList[:6]
		if len(keywordSet) < 3:
			return (str(len(keywordSet))+" keywords in subject. Prerequisite knowledge not required.", "")

	for each in keywordSet:
		if each != subject:
			text = extractTextData(each)
			summ += "\n\n"+each+":\n"
			summ += textRankDriver(text)

	return (subject, summ)
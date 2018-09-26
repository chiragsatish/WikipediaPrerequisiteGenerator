from urllib.request import urlopen
from collections import Counter
from bs4 import BeautifulSoup # A library in python to extract the data from html, xml documents
import re
import datetime
import string
from urllib.parse import unquote
from rake_nltk import Rake
import RAKE
import operator
import wikipedia
import wikipediaapi

# Function to extract info and rank the keywords in a list
def extractKeywordsUsingRake(subject,num_char=3, num_words=3, num_freq=2):
	stoppath = 'smartStopList.txt'
	Rake = RAKE.Rake(RAKE.SmartStopList())
	#Wikipedia module exract page content from wiki page
	extractedText = wikipedia.page(subject).content
	#(number of char in keyword, upto how many words, min freq of keyword) 
	res = Rake.run(extractedText,num_char,num_words,num_freq)
	return res

def keyword_filtering(dataList, linkList):
	temp = [i[0] for i in dataList]
	#keywordSet contains common keywords i.e between hyperlink and rake extracted keywords
	keywordSet_temp = set([x for x in linkList if x.lower() in temp])
	return keywordSet_temp

def keyword_filtering_category(subject, keywordSet_temp):
	cat_mainPage = wikipedia.page(subject).categories
	filtered_cat_mainPage = filterCat(cat_mainPage)
	keywordSet =[]
	for word in list(keywordSet_temp):
		try:
			cat_keywordPage = wikipedia.page(word).categories
		except wikipedia.exceptions.PageError:
			pass
		filtered_cat_keywordPage = filterCat(cat_keywordPage)
		match = Compare(filtered_cat_mainPage, filtered_cat_keywordPage)
		if match:
			keywordSet.append(word)
	return keywordSet
	
# Text Processing for enforcing encodings
def cleanupLatinEncoding(word):
    try:
        return unquote(word, errors='strict')
    except UnicodeDecodeError:
        return unquote(word, encoding='latin-1')

# A function to get urls within the page
def getLinks(url):
	# Append the url tag to wiki
	html = urlopen("https://en.wikipedia.org"+url)
	bsObj = BeautifulSoup(html, "lxml")
	newLinks = list()
	# The url tags are always i) found in bodycontent tag
	for each in bsObj.findAll("div", {"id": "bodyContent"}):
		# ii) start with /wiki/
		# and iii) do not contain semicolons
		for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
			if 'href' in link.attrs:
				#print(link)
				stripped = re.sub('/wiki/', "", link.attrs['href'])
				stripped = re.sub('_', " ", stripped)
				stripped = cleanupLatinEncoding(stripped)
				newLinks.append(stripped)
	return newLinks

# A function to create the link in parsable format
# wikipedia url is in the form : https://en.wikipedia.org/wiki/Papa_CJ
def linkify(s):
	starting = '/wiki/'
	tokens = s.split(" ")
	for i in range(0, len(tokens)):
		# To append the underscore
		if i != 0:
			starting = starting + '_'
		# To append the words
		starting = starting+tokens[i]
	return starting

# A function to extract initial summary of the wiki article
def extractTextData(keyword):
	text =  wikipedia.summary(keyword)
	return text

#Filters the category list  
def filterCat(cat_list):
	flag = 0
	final_cat = []
	l = ['wikipedia', 'Articles', 'Wikipedia', 'articles', 'Use', 'Webarchive', 'Pages', 'Page']
	#l =[]
	for word in list(cat_list):
		l2 = word.split(" ")
		for each in list(l2):
			if each in l:
				flag = 1
				break 
		if flag == 0:
			final_cat.append(word)
		flag = 0
	
	return final_cat

#To compare the categories of candidate keywords with that of the main personality page
#[ x for x in l if "2" in x ]
def Compare(main_list, keyword_list):
	x = []
	x2 = []
	for each in main_list:
		Each = str(each)
		matching = [s for s in keyword_list if Each in s]
		x.append(matching)

	for each in keyword_list:
		Each = str(each)
		matching = [s for s in main_list if Each in s]
		x.append(matching)

	Match = list(set(main_list) & set(keyword_list))
	x.append(Match)
		
	for sublist in x:
		for item in sublist:
			x2.append(item) 

	if len(x2) > 0:
		return True
	else:
		return False   		





		



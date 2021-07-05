# -*- coding: utf-8 -*-
import json
import csv
from spellchecker import SpellChecker
import re
import collections
import nltk
import pyexcel as pe
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()
spell = SpellChecker()
stop_words = set(stopwords.words('english'))
tweets_data_path = 'twitter_data.txt'
file2write=open("twitter_result.txt",'w')
file2words=open("words.txt",'w')
out = open('RESUILT.csv', 'w')
tweets_data = []
tot=""
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        s=tweet.get("text")
        g=s
        print("---------------BEFOR PROCCESSING-------------------")
        print(s)
        tokens=s.split();
        
        #Replace slang and abbreviations(1)
        for word in tokens:
            fileName = "slang.txt"
            accessMode = "r"
            with open(fileName, accessMode) as myCSVfile:
                dataFromFile = csv.reader(myCSVfile, delimiter="=")
               
                for row in dataFromFile:
                    if word.upper() == row[0]:
                      s=s.replace(' '+word+' ',' '+row[1]+' ')
                myCSVfile.close()
        print("---------------AFTER REPLACING ABIREVATIONS-------------------")
        print(s)
        #Replace slang and abbreviations(2)
        tokens=s.split();
        for word in tokens:
            fileName = "cons.txt"
            accessMode = "r"
            with open(fileName, accessMode) as myCSVfile:
                dataFromFile = csv.reader(myCSVfile, delimiter="=")
                   
                for row in dataFromFile:
                    if word == row[0]:
                       s=s.replace(' '+word+' ',' '+row[1]+' ')
                myCSVfile.close()
        print("---------------AFTER REPLACING CONTRACTIONS-------------------")
        print(s)
        #basic noise removing(3)
        s=(s.encode('ascii', 'ignore')).decode("utf-8")
        print("---------------AFTER REMOVING NOISE-------------------")
        print(s)
        #Removing Numbers(4)
        for i in s:
            if i.isdigit():
                s=s.replace(i,'');
        print("---------------AFTER REMOVING NUMBERS-------------------")
        print(s)
        #Removing hash tags(5)
        s=s.replace('#','');
        print("---------------AFTER REMOVING # TAGS-------------------")
        print(s)
        #Removing URL's(6)
        s=re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', s, flags=re.MULTILINE)
        print("---------------AFTER REMOVING LINKS-------------------")
        print(s)
        #Replacing Elongated words(10)
        misspelled = spell.unknown(s.split())
        for word in misspelled:
            s=s.replace(' '+word+' ',' '+re.sub(r'(.)\1+', r'\1', word)+' ')             
        print("---------------AFTER ELONGATED WORDS-------------------")
        print(s)
        #Spelling Correction(14)
        misspelled = spell.unknown(s.split())
        for word in misspelled:
            s=s.replace(' '+word+' ',' '+spell.correction(word)+' ')
        print("---------------AFTER SPELLING CORRECTION-------------------")
        print(s) 
        #Replasing Repetitions of punctuations
        s = re.sub(r'(\W)(?=\1)', '', s)
        print("---------------AFTER REPLACING OF PUNCTUATIONS-------------------")
        print(s)
        
        #Removing @,RT and Stropwords(7)
        tokens=s.split();
        for word in tokens:
            if word.startswith('@') or word=='RT':  
               s= s.replace(word,'')
            if word.lower() in stop_words:
               s=s.replace(' '+word+' ',' ')
        print("---------------AFTER REMOVING @,RT and STOP WORDS-------------------")
        print(s)  
        #Capitalizing Each words(8)
        s=s.title()
        print("---------------AFTER CAPITALIZING EACH WORD-------------------")
        print(s)  
        #lowercase(9)
        s=s.lower()
        print("---------------AFTER LOWERCASE-------------------")
        print(s)  
        
        #Replacing Negations with antonyms(11)
        tokens=s.split();
        for word in tokens:
            for syn in wordnet.synsets(word):
                for lm in syn.lemmas():
                    if lm.antonyms():
                        s=s.replace(word,lm.antonyms()[0].name())
        print("---------------AFTER REPLACING NEGATIONS WITH ANTONYMS-------------------")
        print(s)
        #Replace Stemming(12)
        tokens=s.split();
        for word in tokens:
            s=s.replace(word, stemmer.stem(word))
        print("---------------AFTER REPLACING STEMMING-------------------")
        print(s)
        #Replace Lemmatization(13)
        tokens=s.split();
        for word in tokens:
            s=s.replace(word, lemmatiser.lemmatize(word))
            file2words.writelines('%s,'%word)
        print("---------------AFTER LEMMATIZATION-------------------")
        print(s)
           
        
        #Finally
        i=0;
        tweets_data.insert(i,[g,s])
        tot=tot+" "+s
        i+=1;
    except:
        continue
print(len(tweets_data))
print(tweets_data)
sheet = pe.Sheet(tweets_data)
sheet.save_as("RESUILT.csv")
print("=============RESULT==========")
print(tot)
tot=re.sub('\W+'," ", tot )

sentence = tot
words = sentence.split()
sum=0
c=0;
word_counts = collections.Counter(words)
for word, count in sorted(word_counts.items()):
    sum=sum+count
    c+=1
    print('"%s" is repeated %d time%s.' % (word, count, "s" if count > 1 else ""))
print("count sum:%s"%sum)
print("minimum support :%s"%(sum/c))
word_counts = collections.Counter(words)
for word, count in sorted(word_counts.items()):
    
    if count > (sum/c):
        file2write.writelines('%s,' % (word))
        
file2write.close()
file2words.close()       



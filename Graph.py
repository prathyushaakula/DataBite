import networkx as nx
import matplotlib.pyplot as plt
from textblob import Word
import csv
synonyms=[]
words=[]
# / reading files/

with open('twitter_result.txt','r') as file:
    for w in file:
        words=w.split(",")
words.remove('')
print(words)
G=nx.Graph()

for aword in  words:
    if not aword in  words:
        words.append(aword)
        G.add_node(aword)
            
for word1 in  words:
    for word2 in  words:
        tweets = open('RESUILT.csv', 'r',encoding='ISO-8859-1')
        for t in csv.reader(tweets):
            tweet=t[1] 
            print(tweet)
            if word1 in tweet and word2 in tweet: 
                G.add_edge(word1,word2)

print(G.nodes(data=True))
pos = nx.spring_layout(G,k=1)
nx.draw(G, pos, font_size=16, with_labels=True)

plt.savefig("path.png")

import nltk
import re
from nltk import pos_tag
from scipy.stats import pearsonr
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from pattern.en import pluralize, singularize
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
analyzer = SentimentIntensityAnalyzer()

def cleaning(text):
    sent_text = nltk.sent_tokenize(text)
    n = 0
    cleaned_sentences = []
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        #print(n)        
        cleaned_tokens = []
        for word in tokenized_text:
            word = re.sub(r'[^a-zA-Z0-9-]+', '', word)
            word = word.lower()
            if word != '':
                n += 1
                cleaned_tokens.append(word)
        cleaned_sentences.append(cleaned_tokens)
    return cleaned_sentences,n
                
def getWords(sentences):
    words = set()
    for sentence in sentences:
        pos = pos_tag(sentence)
        for word,postag in pos:
            if postag.startswith('NN'):        
                word = singularize(word) 
                word = lemmatizer.lemmatize(word)
                words.add(word)
    return words
                
def getWordCount(sentences,n):
    wordCount = dict()
    for sentence in sentences:
        pos = pos_tag(sentence)
        for word,postag in pos:
            if postag.startswith('NN'):  
                word = singularize(word) 
                word = lemmatizer.lemmatize(word)    
                if word in wordCount.keys():
                    wordCount[word] += 1
                else:
                    wordCount[word] = 1
    for word in wordCount:
        wordCount[word] /= n
    return wordCount

with open("data/A1.txt", encoding="utf8", errors='ignore') as f:
    text1 = f.read()
    cleaned,n = cleaning(text1)
    X_set = getWords(cleaned)
    wordCount1 = getWordCount(cleaned,n)
    wordCount1 = dict(sorted(wordCount1.items(), key=lambda item: item[1], reverse = True))

with open("Results/keyword/A1summary.txt", encoding="utf8", errors='ignore') as f:
    text2 = f.read()
    cleaned,n = cleaning(text2)
    Y_set = getWords(cleaned)
    wordCount2 = getWordCount(cleaned,n)
    wordCount2 = dict(sorted(wordCount2.items(), key=lambda item: item[1], reverse = True))    

data1 = []
data2 = []
for word in wordCount2:
    if word in wordCount1.keys():
        data1.append(wordCount1[word])
    else:
        data1.append(0)
    data2.append(wordCount2[word])
corr, _ = pearsonr(data1, data2)
print('Pearsons correlation: %.3f' % corr)

score = textstat.gunning_fog(text1)
print("The gunning fog index of text1 is ",score)
score = textstat.gunning_fog(text2)
print("The gunning fog index of text2 is ",score)


l1 = []
l2 = []
  
rvector = X_set.union(Y_set) 
for w in rvector:
    if w in X_set: l1.append(1)
    else: l1.append(0)
    if w in Y_set: l2.append(1)
    else: l2.append(0)
c = 0
  
#cosine formula 
for i in range(len(rvector)):
        c+= l1[i]*l2[i]
cosine = c / float((sum(l1)*sum(l2))**0.5)
print("Cosine similarity: ", cosine)

def jaccard_sim(str1, str2): 
    a = set(str1) 
    b = set(str2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

print("Jaccard similarity is ", jaccard_sim(X_set,Y_set))

vs = analyzer.polarity_scores(text1)
print("Sentiment of text1: ",vs)
vs = analyzer.polarity_scores(text2)
print("Sentiment of text2: ",vs)

    

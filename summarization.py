import nltk
import string
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk import pos_tag
from pattern.en import pluralize, singularize
from nltk.corpus import wordnet
import sys

def Sort(sub_li):
    return(sorted(sub_li, key = lambda x: x[1], reverse = True))

#Creates a tuple for each sentence with number of bonds with preceeding and succeeding sentences
def bondMatrixTuple(matrix,n):
    bond = [ [0]*2 for i in range(n)]
    i = 0
    while i < n:
        precede = 0
        succeed = 0
        index = 0
        while index<n:
            if matrix[i][index] >= 1:
                if index < i:
                    succeed += 1
                elif index > i:
                    precede += 1
            index += 1
        bond[i][0] = succeed
        bond[i][1] = precede
        i += 1
    return bond

#Classify sentence into topic-opening, topic-closing, middle
def classifySentences(bond,imp,avg,n):
    i = 0
    opening = list()
    closing = list()
    middle = list()
    for i in imp:
        if bond[i][0]-bond[i][1]>avg:
            opening.append([i,bond[i][0]+bond[i][1]])
        elif bond[i][1]-bond[i][0]>avg:
            closing.append([i,bond[i][0]+bond[i][1]])
        else:
            middle.append([i,bond[i][0]+bond[i][1]])
    return opening, closing, middle
        
#Get list of synonyms
def getsynonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return set(synonyms)

#Get list of antonyms
def getantonym(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return set(antonyms)

#Get the external keyword list
with open("data/keywords.txt", encoding="utf8", errors='ignore') as f:
    text = f.read()
    keywords = text.split("\n")

print("Enter file name of text to be summarized")
file = input()
with open("data/"+file+".txt", encoding="utf8", errors='ignore') as f:
    text = f.read()
    print("1.Use the Covid-19 keyword list")
    print("2.Use the POS tagging method")
    choice = int(input())
    sent_text = nltk.sent_tokenize(text)    #tokenize the text into sentences
    n = 0
    cleaned_sentences = []
    for sentence in sent_text:
        n += 1
        tokenized_text = nltk.word_tokenize(sentence)  #tokenize the sentence into words     
        cleaned_tokens = []
        for word in tokenized_text:
            word = re.sub(r'[^a-zA-Z0-9-]+', '', word)  #Remove punctuations except hyphen
            word = word.lower()                         #Convert to lowercase
            if word != '':
                cleaned_tokens.append(word)
        tokens_tag = pos_tag(cleaned_tokens)            #Get POS tagging
        if choice == 1:
            filtered_sentence = [w for w in cleaned_tokens if w in keywords or singularize(w) in keywords]
        elif choice == 2:
            filtered_sentence = []
            for w,postag in tokens_tag:
                if postag.startswith('NN'):             #Filter nouns
                    filtered_sentence.append(w)
        else:
            exit()
        cleaned_sentences.append(filtered_sentence)
    link_matrix = [ [0]*n for i in range(n)]
    bond_matrix = [ [0]*n for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            ct = 0
            for w1 in cleaned_sentences[i]:
                for w2 in cleaned_sentences[j]:
                    if w1 == w2:            #Simple repetition
                        ct += 1
                    elif w1 == singularize(w2) or singularize(w1) == w2: #Simple repetition
                        ct += 1
                    elif w1 == pluralize(w2) or pluralize(w1) == w2: #Simple repetition
                        ct += 1
                    elif lemmatizer.lemmatize(w1) == lemmatizer.lemmatize(w2): #Complex repetition
                        ct += 1
                    elif w2 in getsynonym(w1):                      #Simple paraphrase
                        ct += 1
                    elif w2 in getantonym(w1):                      #Complex paraphrase
                        ct += 1
            link_matrix[i][j] = ct
            link_matrix[j][i] = ct
    ct = 0
    for i in range(n):
        for j in range(n):
            if link_matrix[i][j] >= 3 and i!=j:     #bond if link>=3
                bond_matrix[i][j] = 1
                ct += 1
            else:
                bond_matrix[i][j] = 0
    average_bond = ct/n
    summary= []
    imp = []
    for i in range(n):
        if sum(bond_matrix[i])>3:
            imp.append(i) 
    bond = bondMatrixTuple(bond_matrix,n)
    opening, closing, middle = classifySentences(bond,imp,average_bond,n)
    opening = Sort(opening)
    closing = Sort(closing)
    middle = Sort(middle)
    sent = []
    if n<100:
        size = 1
    else:
        size = 2
    for i in range(len(opening)):
        if i<3*size:
            sent.append(opening[i][0])
    for i in range(len(middle)):
        if i<4*size:
            sent.append(middle[i][0])
    for i in range(len(closing)):
        if i<3*size:
            sent.append(closing[i][0])
    sent= sorted(sent)
    for i in sent:
        summary.append(sent_text[i])
        
    summary = ' '.join(summary)
    print(summary)
    if choice == 1:
        with open("Results/keyword/"+file+"summary.txt", "w") as text_file:
            text_file.write(summary)
    elif choice == 2:
        with open("Results/pos/"+file+"summary.txt", "w") as text_file:
            text_file.write(summary)

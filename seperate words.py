"""
Created     : Thu Jul 26 2019
Modified    : Tue Jul 30 2019
Author      : S.Nagarakshana
Student No  : PS/2015/342

"""

from nltk.tokenize import word_tokenize

def lowercase_RemStopWord_func(original,afterRemoved,lowercase):
    """open the original article"""
    f=open(original,"r")
    file=f.read()
    f.close()
    
    """converting the letters in the original article to lowercase letters"""
    low = file.lower()
    
    """writing the converted article in lowercase txt file"""
    t1=open(lowercase,"w")
    t1.write(low)
    t1.close()
    
    """open the stopwords.txt file"""
    f_stop = open("stopwords.txt","r")
    stop_word_set = f_stop.read();
    
    """to seperate the words in the stop_word_set and low """
    stop_words = word_tokenize(stop_word_set)
    words = word_tokenize(low)
    
    """remove all the stopwords and write the remaining in afterRemoved txt file"""
    t=open(afterRemoved,"w")
    for word in words:
        if word not in stop_words:
            t.write(word+"\n")
            
    t.close()
     

"""for loop to call the lowercase_RemStopWors_func for all 150 articles"""
#note that all the original articles should be in the same location as the code
for i in range(1,151):  
    lowercase_RemStopWord_func("article_"+str(i)+".txt","remData_"+str(i)+".txt","lowercaseArticle_"+str(i)+".txt")
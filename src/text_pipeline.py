
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re

emotions = pd.read_csv('NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', names=['word', 'emotion', 'association'], skiprows=45, sep='\t')

emotions = emotions[emotions['emotion'] == 'positive']
ss = SnowballStemmer(language='english')
def preprocess(arr):
    '''
    removes puncuation from reviews, puts in lower case
    '''
    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    step1 = [REPLACE_NO_SPACE.sub("", line.lower()) for line in arr]
    step2 = [REPLACE_WITH_SPACE.sub(" ", line) for line in step1]
    return step2

def remove_stopwords(arr):
    stop = stopwords.words('english')
    stop.append('get')
    stop.append('—')
    stop.append('thats')
    stop.append('dont')
    stop.append('us')
    stop.append('im')
    arr = pd.Series(arr).apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    return arr

def stemmer(arr):
    ss = SnowballStemmer(language='english')
    output = list()
    for text in arr:
        current = ""
        for word in text.split():
            current += ss.stem(word) + " "
        output.append(current)
    return output
    
def text_to_vector(arr):
    processed = preprocess(arr)
    stopped = remove_stopwords(processed)
    for idx, i in enumerate(stopped):
        if len(i) <= 5:
            stopped.drop(idx, inplace=True)
        
    ss = SnowballStemmer(language='english')
    vectorizer = CountVectorizer(stop_words='english')
                                 # vocabulary = emotions['word'])
    output = list()
    for text in processed:
        current = ""
        for word in text.split():
            current += ss.stem(word) + " "
        output.append(current)
        
    vector = vectorizer.fit_transform(np.array(output))
    vector_pd = pd.DataFrame(vector.toarray(), columns = vectorizer.get_feature_names())
    return vectorizer, vector, vector_pd
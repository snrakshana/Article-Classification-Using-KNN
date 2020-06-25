import nltk
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('genesis')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
genesis_ic = wn.ic(genesis, False, 0.0)

class KNNClassifer():
    def __init__(self, k=1, distance_type = 'path'):
        self.k = k
        self.distance_type = distance_type

    def fit(self, x_train, y_train):
        """
        Used for training
        Args:
            x_train: list of word corpus
            y_train: list of classes
        """
        print('[INFO] Model training...')
        self.x_train = x_train
        self.y_train = y_train
        print('[INFO] Model training completed\n\n')

    def predict(self, x_test):
        """
        This function runs the K(1) nearest neighbour algorithm and
        returns the label with closest match. 

        Args:
            x_test: 
        """
        self.x_test = x_test
        y_predict = []

        for i in range(len(x_test)):
            max_sim = 0
            max_index = 0
            for j in range(len(self.x_train)):
                temp = self.document_similarity(x_test[i], self.x_train[j])
                if temp > max_sim:
                    max_sim = temp
                    max_index = j
            y_predict.append(self.y_train[max_index])
            print('[INFO] {} of {} completed'.format(i+1, len(x_test)))
        return y_predict

    def convert_tag(self, tag):
        """
        Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets
        If there is no match returns None

        Args:
            tag: nltk.pos_tag

        Returns:
            tag used by wordnet.synsets
        """
        tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
        try:
            return tag_dict[tag[0]]
        except KeyError:
            return None


    def corpus_to_synsets(self, corpus):
        """
        Returns a list of synsets (synonyms) in corpus.
        Tags the words in the corpus.
        Then finds the first synset for each word/tag combination.
        If a synset is not found for that combination it is skipped.

        Args:
            corpus: list of words

        Returns:
            list of synsets
        """

        l = []
        tags = nltk.pos_tag(corpus)
        
        for word, tag in zip(corpus, tags):
            syntag = self.convert_tag(tag[1])
            syns = wn.synsets(word, syntag)
            if (len(syns) > 0):
                l.append(syns[0])
        return l 
    
    def doc_to_synsets(self, doc):
        """
        Returns a list of synsets (synonyms) in document.
        Tokenizes and tags the words in the document doc.
        Then finds the first synset for each word/tag combination.
        If a synset is not found for that combination it is skipped.

        Args:
            doc: string to be converted

        Returns:
            list of synsets
        """
        tokens = word_tokenize(doc)
        
        l = []
        tags = nltk.pos_tag([tokens[0] + ' ']) if len(tokens) == 1 else nltk.pos_tag(tokens)
        
        for token, tag in zip(tokens, tags):
            syntag = self.convert_tag(tag[1])
            syns = wn.synsets(token, syntag)
            if (len(syns) > 0):
                l.append(syns[0])
        return l  
    
    def similarity_score(self, s1, s2, distance_type='path'):
        """
        Calculate the normalized similarity score of synsets s1 onto s2
        For each synset in s1, finds the synset in s2 with the largest similarity value.
        Sum of all of the largest similarity values and normalize this value by dividing it by the
        number of largest similarity values found.

        Args:
            s1, s2: list of synsets from doc_to_synsets

        Returns:
            normalized similarity score of s1 onto s2
        """
        s1_largest_scores = []

        for i, s1_synset in enumerate(s1, 0):
            max_score = 0
            for s2_synset in s2:
                if distance_type == 'wup':
                    score = s1_synset.wup_similarity(s2_synset)  
                elif distance_type == 'path':
                    score = s1_synset.path_similarity(s2_synset, simulate_root = False)

                if score != None:
                    if score > max_score:
                        max_score = score
            
            if max_score != 0:
                s1_largest_scores.append(max_score)
        
        mean_score = np.mean(s1_largest_scores)
                
        return mean_score  

    def document_similarity(self, doc, corpus):
        """
        Finds the symmetrical similarity between the given and text corpus
        """

        synsets1 = self.doc_to_synsets(doc)
        synsets2 = self.corpus_to_synsets(corpus)
        
        return (self.similarity_score(synsets1, synsets2) + self.similarity_score(synsets2, synsets1)) / 2

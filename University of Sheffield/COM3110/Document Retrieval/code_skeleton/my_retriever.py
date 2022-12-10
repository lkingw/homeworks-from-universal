import math

maxRereivalNum = 10

class Retrieve:
    
    # Create new Retrieve object storing index and term weighting
    # scheme. (You can extend this method, as required.)
    def __init__(self, index, term_weighting):
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        self.idfScore = self.getIDF()
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        return len(self.doc_ids)

    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        #Declare variables to be used in the program, adding 1 so that the index matches the articleID
        bestArticles, articleMat, freqSum = [], ([0] * (self.num_docs + 1)), ([0] * (self.num_docs + 1))

        if (self.term_weighting == 'binary'):
            # compute binary weight of each term for each article
            for key in query:
                if key in self.index:
                    for article, _ in self.index[key].items(): articleMat[article] += 1

            #get vector size
            for word in self.index.keys():
                for article, freq in self.index[word].items():
                    freqSum[article] += 1
            sqrfreqSum = [math.sqrt(x) for x in freqSum]

            # compute Cosine similarity using Binary term weighting
            for number in range(1, self.num_docs): articleMat[number] = articleMat[number] / sqrfreqSum[number]
            # return top articles
            return self.topArticles(articleMat)


        elif (self.term_weighting == 'tf'):
            #Computing the terms that are both in the query and article
            for word in list(set(query)):
                if word in self.index:
                    for article,freq in self.index[word].items():
                        articleMat[article] += freq * query.count(word)

            # Compute vector size
            for word in self.index.keys():
                for article, freq in self.index[word].items():
                    freqSum[article] += math.pow(freq, 2)
            sqrfreqSum =[math.sqrt(x) for x in freqSum]

            # Compute Cosine similarity using TF term weighting
            for number in range(1, self.num_docs): articleMat[number] = articleMat[number] / sqrfreqSum[number]
            # return top articles
            return self.topArticles(articleMat)

        elif (self.term_weighting == 'tfidf'):
            # Computing the terms that are both in the query and article
            for key in list(set(query)):
                if key in self.index:
                    for article, freq in self.index[key].items():
                            articleMat[article] += freq * query.count(key) * math.pow(self.idfScore[key],2)

            # Compute vector size
            for word in self.index.keys():
                for article, freq in self.index[word].items():
                    freqSum[article] += math.pow(freq*(self.idfScore[word]), 2)
            sqrfreqSum = [math.sqrt(x) for x in freqSum]

            # Compute Cosine similarity using TFIDF term weighting
            for number in range(1, self.num_docs): articleMat[number] = articleMat[number] / sqrfreqSum[number]
            # return top articles
            return self.topArticles(articleMat)

    #Extract the indexes of the top 10 scoring articles
    def topArticles(self, articleMat):
        bestArticles = []
        for x in range(maxRereivalNum):
            indexOfMaxValue = articleMat.index(max(articleMat))
            bestArticles.append(articleMat.index(max(articleMat)))
            articleMat[indexOfMaxValue] = 0
        return bestArticles

    #Comnpute the maximum number of articles in the set
    def maxArticles(self):
        num_docs = 0
        for word in self.index.keys():
            for article in self.index[word]:
                if article > num_docs:
                    num_docs = article
        return num_docs

    #Compute the IDF weight
    def getIDF(self):
        idfScore = dict()
        for term in self.index:
            idfScore[term] = math.log(self.num_docs / len(self.index[term].items()))
        return idfScore
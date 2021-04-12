import sys
import random
from DTF import DecisionTreeClassifier

class RandomForestClassifier(object):

    def __init__(self, n_estimators =  32, bootstrap = 1, minleaf = 1):
        """
        Args:
            n_estimators: The number of decision trees in the forest.
            bootstrap: The fraction of randomly choosen data to fit each tree on.
        """
        self.n_estimators = n_estimators
        self.bootstrap = bootstrap
        self.forest = []
        self.minleaf = minleaf


    def fit(self, data, fields):
        """ Creates a forest of decision trees using a random subset of data and
            features. """

        self.forest = []
        for i in range(self.n_estimators):
            sample_data = {}
            sample_num = self.bootstrap * len(data['f_acid'])
            #index_list = list(range(len(data['f_acid'])))
            sample_list = []
            for i in range(int(sample_num)):
                sample_list.append(random.randint(0, len(data['f_acid']) - 1))
            #sample_list = random.sample(index_list, int(sample_num))
            
            for field in fields:
                dl = []
                for i in sample_list:
                    d = data[field][i]
                    dl.append(d)
                sample_data[field] = dl

            tree = DecisionTreeClassifier(sample_data, fields[0:-1], 'quality', self.minleaf)
            self.forest.append(tree)


    def predict(self, X):

        """ Predict the class of each sample in X. """
        meta_list = []
        for i, v in enumerate(X['f_acid']):
            meta = {}
            for key in list(X.keys()):
                if key != 'quality':
                    meta[key] = X[key][i]
            meta_list.append(meta)

        n_trees = len(self.forest)
        result = []
        for i, row in enumerate(meta_list):
            predictions = []
            for j in range(n_trees):
                p = self.forest[j].predict(self.forest[j].root, row)
                if p != 'unknown':
                    predictions.append(p)
            if len(predictions) > 0:
                result.append(max(set(predictions), key=predictions.count))
            else:
                result.append('5')
            #print(predictions, max(set(predictions), key=predictions.count))
        return result


    def score(self, X, y):
        """ Return the accuracy of the prediction of X compared to y. """
        y_predict = self.predict(X)
        n_samples = len(y)
        correct = 0
        for i in range(n_samples):
            if y_predict[i] == y[i]:
                correct += 1
        return float(correct) / float(n_samples)

    
    def slices(self, sentence):

        metas = []
        temp_word = ''
        for i in range(len(sentence)):
            if sentence[i] not in (' ', '\n', '\r'):
                temp_word += sentence[i]
            else:
                if len(temp_word) > 0:
                    metas.append(temp_word)
                    temp_word = ''

        return metas


    def fwf_file_parse(self, file, type):
        
        data_dict = {}
        data = open(file)
        counter = 0
        fields = []
        for line in data:
        
            meta = list(self.slices(line))
            meta = map(lambda x: x.replace(' ','').replace('\n','').replace('\r',''), meta)
            if counter == 0:
                for field_name in meta:
                    data_dict[field_name] = []
                fields = meta
            else:
                for i, value in enumerate(meta):
                    if i != 11: data_dict[fields[i]].append(float(value))
                    else: 
                        hehe = int(value)
                        data_dict[fields[i]].append(value)
            counter += 1

        return fields, data_dict


if __name__ == '__main__':

    args = (sys.argv)

    trainFile = args[1]
    testFile = args[2]
    minleaf = args[3]
    n_tree = args[4]
    random_seed = args[5]

    random.seed(float(random_seed))

    forest = RandomForestClassifier(n_estimators = int(n_tree), minleaf = int(minleaf))
    fields, trainData = forest.fwf_file_parse(trainFile, 'train')
    _, testData = forest.fwf_file_parse(testFile, 'test')
    forest.fit(trainData, fields)

    accuracy = forest.score(trainData, trainData['quality'])
    print(accuracy)

    classifications = forest.predict(testData)
    for i in range(len(classifications)):
        print(classifications[i])
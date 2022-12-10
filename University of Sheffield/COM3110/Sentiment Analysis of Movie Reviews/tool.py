import pandas as pd
import numpy as np
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

class SentimentScales:
    scale_3 = [ 'negative', 'neutral' , 'positive' ]

    scale_5 = [ 'negative', 'somewhat negative', 'neutral', 'somewhat positive', 'positive' ]

class Phrase:

    def __init__(self, id, tokens, sentiment):
        self.id = id
        self.tokens = tokens
        self.sentiment = sentiment

    @classmethod
    def load_phrases(cls, filename):
        phrases = []
        df = pd.read_csv(filename, index_col=0, delimiter='\t')

        parse_sentiment = 'Sentiment' in df.columns

        for index, row in df.iterrows():
            if parse_sentiment:
                phrase = Phrase(index, row['Phrase'].split(), row['Sentiment'])
            else:
                phrase = Phrase(index, row['Phrase'].split(), -1)
            phrases.append(phrase)
        return phrases

class Preprocessor:

    def __init__(self, phrases):
        self.phrases = phrases
        
        # Init stopwords
        self.stoplist = stopwords.words('english')
        self.stoplist.extend(string.punctuation.replace('!', ''))
        self.stoplist.extend([ '\'s', '``', '\'\'', '...', '--', 'n\'t', '\'d' ])
        self.stoplist = set(self.stoplist)

        # Init Stemmer (removed)
        # self.stemmer = SnowballStemmer('english')

        # Init sentiment scale mapping
        self.scale_5_3 = {
            0:0,
            1:0,
            2:1,
            3:2,
            4:2
        }

    def preprocessing(self):
        for phrase in self.phrases:
            # Capitalisation
            phrase.tokens = [i.lower() for i in phrase.tokens ]

            # Stemming (Removed)
            # phrase.tokens = [self.stemmer.stem(i) for i in phrase.tokens ]

            # Stopword removal
            phrase.tokens = [i for i in phrase.tokens if i not in self.stoplist ]

        return self.phrases

    def to_scale_3(self):
        for phrase in self.phrases:
            if phrase.sentiment < 0:
                # Not available
                continue
            phrase.sentiment = self.scale_5_3[phrase.sentiment]
        return self.phrases

class FeatureProcessor:

    def __init__(self, features=[], trimming_ratio=0.2, dump_sorted_terms_biases=False):
        self.features = features
        self.trimming_ratio = trimming_ratio

        # Dump sorted_terms_biases (Debug)
        self.dump_sorted_terms_biases = dump_sorted_terms_biases

    def extract_features(self, phrases, scale):
        # Count the number of times each token appears in different sentiment
        token_sentiment_counts_dict = dict()
        for phrase in phrases:
            sentiment = phrase.sentiment
            for token in phrase.tokens:
                if token not in token_sentiment_counts_dict:
                    token_sentiment_counts_dict[token] = [0] * scale
                token_sentiment_counts_dict[token][sentiment] += 1

        # Filter out tokens with too few occurrences
        # token_sentiment_counts = [(term, sentiment_counts) for term, sentiment_counts in token_sentiment_counts_dict.items() if sum(sentiment_counts) > scale]

        # Calculate the sentiment bias of each token
        sentiment_biases = []
        for token, sentiment_counts in token_sentiment_counts_dict.items():
            sentiment_bias = 0

            # Calulate sentiment_bias 
            # Neutral sentiment weights 0, Positive sentiment weights positive value, Negative sentiment weights negative value
            for i in range(scale):
                factor = i - (scale - 1) / 2
                sentiment_bias += sentiment_counts[i] * factor

            # Normalization
            # sentiment_bias = sentiment_bias / sum(sentiment_counts)
            # sentiment_bias = sentiment_bias * sentiment_bias

            sentiment_biases.append((token, sentiment_bias))
        
        # Sort list based on sentiment bias
        sorted_terms_biases = sorted(sentiment_biases, key=lambda item: item[1] * item[1], reverse=True)

        # Dump sorted_terms_biases (Debug)
        if self.dump_sorted_terms_biases:
            f = open('sorted_terms_biases.txt', 'w')
            for b in sorted_terms_biases:
                f.write(str(b[1]) + '\t' + b[0] + '\n')
            f.close()
        
        # Trim features list
        trim_length = int(len(sentiment_biases) * self.trimming_ratio)
        trimed_sorted_terms_biases = sorted_terms_biases[:trim_length]
        self.features = [i[0] for i in trimed_sorted_terms_biases]
        return self.features

    def filter_features(self, phrases):
        for phrase in phrases:
            phrase.tokens = [i for i in phrase.tokens if i in self.features ]
        return phrases

#==============================================================================
# Training

class CorpusMeta:

    def __init__(self, phrases, sentiment_scale):
        self.sentiment_scale = sentiment_scale
        self.phrase_count = len(phrases)
        self.sentiment_phrase_counts = self.__compute_sentiment_phrase_counts(phrases, sentiment_scale)
        self.sentiment_token_counts = self.__compute_sentiment_token_counts(phrases, sentiment_scale)
        self.relative_sentiment_token_counts = self.__compute_relative_sentiment_token_counts(phrases, sentiment_scale)
        self.vocabulary_count = self.__compute_vocabulary_count(phrases)

    def __compute_sentiment_phrase_counts(self, phrases, scale):
        phrase_counter = Counter()

        for phrase in phrases:
            sentiment = phrase.sentiment
            phrase_counter[sentiment] += 1

        phrase_counts = []
        for i in range(len(scale)):
            phrase_counts.append(phrase_counter[i])

        return phrase_counts

    def __compute_sentiment_token_counts(self, phrases, scale):
        token_counter = Counter()

        for phrase in phrases:
            sentiment = phrase.sentiment
            token_counter[sentiment] += len(phrase.tokens)

        phrase_counts = []
        for i in range(len(scale)):
            phrase_counts.append(token_counter[i])

        return phrase_counts

    def __compute_relative_sentiment_token_counts(self, phrases, scale):
        relative_counters = []
        for i in range(len(scale)):
            relative_counters.append(Counter())

        for phrase in phrases:
            sentiment = phrase.sentiment
            for token in phrase.tokens:
                relative_counters[sentiment][token] += 1
        
        relative_counts = []
        for i in range(len(scale)):
            count_dict = dict(relative_counters[i])
            relative_counts.append(count_dict)
        
        return relative_counts
    
    def __compute_vocabulary_count(self, phrases):
        vocabulary = set()
        for phrase in phrases:
            vocabulary.update(phrase.tokens)
        return len(vocabulary)
            
#==============================================================================
# Pridicting

class Predictor:

    def __init__(self, corpus_meta):
        self.corpus_meta = corpus_meta

    def predict_likelihoods(self, phrases):
        corpus_meta = self.corpus_meta
        results = []
        for phrase in phrases:
            likelihoods = []
            for i in range(len(corpus_meta.sentiment_scale)):
                sentiment_phrase_count = corpus_meta.sentiment_phrase_counts[i]
                if corpus_meta.sentiment_phrase_counts[i] > 0:
                    # prior probability
                    prob = sentiment_phrase_count / corpus_meta.phrase_count

                    # relative likelihoods
                    relative_token_counts = corpus_meta.relative_sentiment_token_counts[i]
                    sentiment_token_count = corpus_meta.sentiment_token_counts[i]
                    smoothed_sentiment_token_count = sentiment_token_count + corpus_meta.vocabulary_count
                    for token in phrase.tokens:
                        if token in relative_token_counts:
                            relative_token_count = relative_token_counts[token]
                        else:
                            relative_token_count = 0
                        smoothed_relative_token_count = relative_token_count + 1
                        token_prob = smoothed_relative_token_count / smoothed_sentiment_token_count
                        prob *= token_prob
                    likelihoods.append(prob)
                else:
                    likelihoods.append(0)
            results.append(likelihoods)
        return results

    def predict(self, phrases):
        results = []
        likelihoods_list = self.predict_likelihoods(phrases)
        for likelihoods in likelihoods_list:
            argmax = max(range(len(likelihoods)), key=lambda x: likelihoods[x])
            results.append(argmax)
        return results

#==============================================================================
# Evaluation

class Evaluator:

    def __init__(self, phrases, predict_result_dict, scale):
        self.accuracy = None
        self.f1 = None
        self.phrases = phrases
        self.predict_result_dict = predict_result_dict
        self.scale = scale

        cf_matrix = [[0] * scale for i in range(scale)]
        for phrase in phrases:
            id = phrase.id
            if id in predict_result_dict:
                cf_matrix[phrase.sentiment][predict_result_dict[id]] += 1
            else:
                print('missing prediction', id)
        
        self.cf_matrix = cf_matrix

    def compute_accuracy(self):
        if self.accuracy != None:
            return self.accuracy
        accurate_count = sum([self.cf_matrix[i][i] for i in range(self.scale)])
        total_count = sum([sum(self.cf_matrix[i]) for i in range(self.scale)])
        accuracy = accurate_count / total_count
        return accuracy

    def compute_f1(self):
        if self.f1 != None:
            return self.f1
        true_pos = np.diag(self.cf_matrix) 
        cf_mat = np.array(self.cf_matrix, dtype=float)
        precision = np.mean(np.divide(true_pos, np.sum(cf_mat, axis=0)))
        recall = np.mean(np.divide(true_pos, np.sum(cf_mat, axis=1), out=np.zeros_like(np.array(true_pos, dtype=float)), where=np.sum(cf_mat, axis=1)!=0))
        return 2 * (precision * recall) / (precision + recall)

    def plot_confusion_matrix(self, target_names=None, title='Confusion matrix', cmap=None):
        cf_matrix = self.cf_matrix
        scale = self.scale
        
        # accuracy = self.compute_accuracy()
        # misclass = 1 - accuracy

        if cmap is None:
            cmap = plt.get_cmap('Blues')

        # plt.figure(figsize=(8, 6))
        # plt.figure(figsize=(4, 3.5))
        plt.figure(figsize=(3, 2.5))
        plt.imshow(cf_matrix, interpolation='nearest', cmap=cmap)
        # plt.title(title)
        plt.colorbar()

        if target_names is not None:
            tick_marks = range(len(target_names))
            plt.xticks(tick_marks, target_names, rotation=45)
            plt.yticks(tick_marks, target_names)
        else:
            tick_marks = range(scale)
            plt.xticks(tick_marks, tick_marks)
            plt.yticks(tick_marks, tick_marks)

        textcolor_thresh = max([max(i) for i in cf_matrix]) / 2
        for i in range(scale):
            for j in range(scale):
                plt.text(j, i, "{:,}".format(cf_matrix[i][j]),
                        horizontalalignment="center",
                        color="white" if cf_matrix[i][j] > textcolor_thresh else "black")

        plt.ylabel('True label')
        # plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.show()
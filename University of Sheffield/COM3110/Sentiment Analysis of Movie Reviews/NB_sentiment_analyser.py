from tool import *
import pandas as pd
import argparse

USER_ID = 'acc19yx'

#==============================================================================
# Command line processing

def parse_args():
    parser=argparse.ArgumentParser(description="A Naive Bayes Sentiment Analyser for the Rotten Tomatoes Movie Reviews dataset")
    parser.add_argument("training")
    parser.add_argument("dev")
    parser.add_argument("test")
    parser.add_argument("-classes", type=int)
    parser.add_argument('-features', type=str, default="all_words", choices=["all_words", "features"])
    parser.add_argument('-output_files', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-confusion_matrix', action=argparse.BooleanOptionalAction, default=False)
    args=parser.parse_args()
    return args


def main(config):
    train_phrases = Phrase.load_phrases(config.training)
    train_preprocessor = Preprocessor(train_phrases)
    train_preprocessor.preprocessing()

    dev_phrases = Phrase.load_phrases(config.dev)
    dev_preprocessor = Preprocessor(dev_phrases)
    dev_preprocessor.preprocessing()

    test_phrases = Phrase.load_phrases(config.test)
    test_preprocessor = Preprocessor(test_phrases)
    test_preprocessor.preprocessing()

    sentiment_scale = SentimentScales.scale_5
    if config.classes == 3:
        sentiment_scale = SentimentScales.scale_3
        train_preprocessor.to_scale_3()
        dev_preprocessor.to_scale_3()
        test_preprocessor.to_scale_3()

    if config.features == "features":
        featureProcessor = FeatureProcessor()
        featureProcessor.extract_features(train_phrases, config.classes)
        featureProcessor.filter_features(train_phrases)
        featureProcessor.extract_features(dev_phrases, config.classes)
        featureProcessor.filter_features(dev_phrases)
        featureProcessor.extract_features(test_phrases, config.classes)
        featureProcessor.filter_features(test_phrases)

    corpus_meta = CorpusMeta(train_phrases, sentiment_scale)

    # output dev prediction

    predictor = Predictor(corpus_meta)
    predicted_results = predictor.predict(dev_phrases)

    dev_file_name = './predictions/' + '_'.join(['dev', 'predictions', str(config.classes) + 'classes', USER_ID]) + ".tsv"
    with open(dev_file_name, 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in range(len(predicted_results)):  
            f.write(str(dev_phrases[i].id) + '\t' + str(predicted_results[i]) + '\n')

    df = pd.read_csv(dev_file_name, index_col=0, delimiter='\t')
    predict_dict = dict()
    for index, row in df.iterrows():
        predict_dict[index] = row['Sentiment']

    # output test prediction

    predicted_results = predictor.predict(test_phrases)

    test_file_name = './predictions/' + '_'.join(['test', 'predictions', str(config.classes) + 'classes', USER_ID]) + ".tsv"
    with open(test_file_name, 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in range(len(predicted_results)):  
            f.write(str(test_phrases[i].id) + '\t' + str(predicted_results[i]) + '\n')

    df = pd.read_csv(test_file_name, index_col=0, delimiter='\t')
    predict_dict = dict()
    for index, row in df.iterrows():
        predict_dict[index] = row['Sentiment']

    # evaluation
    evaluationer = Evaluator(test_phrases, predict_dict, config.classes)
    #accuracy = evaluationer.compute_accuracy()
    f1_score = evaluationer.compute_f1()
    if config.confusion_matrix:
        evaluationer.plot_confusion_matrix()

    print("%s\t%d\t%s\t%f" % (USER_ID, config.classes, config.features, f1_score)) #f1_score))

def get_input():
    
    inputs=parse_args()
    
    #input files
    training = inputs.training
    dev = inputs.dev
    test = inputs.test
    
    #number of classes
    number_classes = inputs.classes
    
    #accepted values "features" to use your features or "all_words" to use all words (default = all_words)
    features = inputs.features
    
    #whether to save the predictions for dev and test on files (default = no files)
    output_files = inputs.output_files
     
    #whether to print confusion matrix (default = no confusion matrix)
    confusion_matrix = inputs.confusion_matrix

    return {
        training,
        dev,
        test,
        number_classes,
        features,
        output_files,
        confusion_matrix
    }
    
    
if __name__ == "__main__":
    inputs=parse_args()
    main(inputs)

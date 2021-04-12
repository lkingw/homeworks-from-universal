import sys
import math
import time


class Node(object):
    def __init__(self, attribute, threshold):
        self.attr = attribute
        self.thres = threshold
        self.left = None
        self.right = None
        self.leaf = False
        self.predict = None


# First select the threshold of the attribute to split set of test data on
# The threshold chosen splits the test data such that information gain is maximized
def select_threshold(df, attribute, predict_attr):

    # Convert dataframe column to a list and round each value
    values = df[attribute]
    values = list(set(values))
    values.sort()
    # Remove duplicate values by converting the list to a set, then sort the set
    max_ig = float("-inf")
    thres_val = 0
    # try all threshold values that are half-way between successive values in this sorted list
    for i in range(0, len(values) - 1):
        thres = 0.5 * (values[i] + values[i+1])
        ig = info_gain(df, attribute, predict_attr, thres)
        if ig > max_ig:
            max_ig = ig
            thres_val = thres
    # Return the threshold value that maximizes information gained
    return thres_val


# Calculate info content (entropy) of the test data
def info_entropy(predict_values, predict_attr):

    df_length = len(predict_values)

    # Dataframe and number of positive/negatives examples in the data
    counter_5 = float(0)
    counter_6 = float(0)
    counter_7 = float(0)

    for d in predict_values:
        if d == '5': counter_5 += 1
        elif d == '6': counter_6 += 1
        else: counter_7 += 1

    # Calculate entropy
    e = float(0)
    if counter_5 != 0: e += ((-1*counter_5)/df_length) * math.log(counter_5/df_length, 2) 
    if counter_6 != 0: e += ((-1*counter_6)/df_length) * math.log(counter_6/df_length, 2)
    if counter_7 != 0: e += ((-1*counter_7)/df_length) * math.log(counter_7/df_length, 2)
    
    return e


# Calculates the weighted average of the entropy after an attribute test
def remainder(df, df_subsets, predict_attr):
    # number of test data
    num_data = float(len(df['quality']))
    remainder = float(0)
    for df_sub in df_subsets:
        if len(df_sub) > 1:
            sub_num = float(len(df_sub))
            remainder += (sub_num / num_data)* info_entropy(df_sub, predict_attr)

    return remainder


# Calculates the information gain from the attribute test based on a given threshold
# Note: thresholds can change for the same attribute over time
def info_gain(df, attribute, predict_attr, threshold):

    sub_1 = []
    sub_2 = []

    for i, d in enumerate(df[attribute]):
        if d <= threshold:
            sub_1.append(df[predict_attr][i])
        else:
            sub_2.append(df[predict_attr][i])    

    # Determine information content, and subract remainder of attributes from it
    ig = info_entropy(df, predict_attr) - remainder(df, [sub_1, sub_2], predict_attr)
    return ig


# Returns the number of positive and negative data
def num_class(df, predict_attr):

    counter_5 = 0
    counter_6 = 0
    counter_7 = 0

    if 'quality' in df:
        for d in df[predict_attr]:
            if d == '5': counter_5 += 1
            elif d == '6': counter_6 += 1
            else: counter_7 += 1

    return [counter_5, counter_6, counter_7]


# Chooses the attribute and its threshold with the highest info gain
# from the set of attributes
def choose_attr(df, attributes, predict_attr):
    max_info_gain = float("-inf")
    best_attr = None
    threshold = 0
    # Test each attribute (note attributes maybe be chosen more than once)
    for attr in attributes:
        thres = select_threshold(df, attr, predict_attr)
        ig = info_gain(df, attr, predict_attr, thres)
        if ig > max_info_gain:
            max_info_gain = ig
            best_attr = attr
            threshold = thres
    return best_attr, threshold


# Builds the Decision Tree based on training data, attributes to train on,
# and a prediction attribute
def build_tree(df, cols, predict_attr, minleaf):

    # Get the number of positive and negative examples in the training data
    nums = num_class(df, predict_attr)
    codes = ['5', '6', '7']

    # If train data has all positive or all negative values
    # then we have reached the end of our tree
    max_value = max(nums)
    max_index = nums.index(max_value)
    max_counter = 0
    zero_counter = 0

    for n in nums:
        if n == max_value: max_counter += 1 
        if n == 0: zero_counter += 1
    if max_counter == 1: code = codes[max_index]
    else: code = 'unknown'

    if zero_counter == 2 or 'quality' not in df or len(df['quality']) <= minleaf:
        # Create a leaf node indicating it's prediction
        leaf = Node(None,None)
        leaf.leaf = True
        leaf.predict = code
        return leaf
    else:
        # Determine attribute and its threshold value with the highest
        # information gain
        best_attr, threshold = choose_attr(df, cols, predict_attr)
        # Create internal tree node based on attribute and it's threshold
        tree = Node(best_attr, threshold)

        sub_1 = {}
        sub_2 = {}
        fields = list(df.keys())

        for i, d in enumerate(df[best_attr]):
            if d <= threshold:
                for f in fields:
                   if f not in sub_1: sub_1[f] = []
                   sub_1[f].append(df[f][i])
            else:
                for f in fields:
                   if f not in sub_2: sub_2[f] = []
                   sub_2[f].append(df[f][i])

        # Recursively build left and right subtree
        tree.left = build_tree(sub_1, cols, predict_attr, minleaf)
        tree.right = build_tree(sub_2, cols, predict_attr, minleaf)
        return tree


# Given a instance of a training data, make a prediction of healthy or colic
# based on the Decision Tree
# Assumes all data has been cleaned (i.e. no NULL data)
def predict(node, row_df):
    # If we are at a leaf node, return the prediction of the leaf node
    # node.leaf

    if node.leaf:
        return node.predict
    # Traverse left or right subtree based on instance's data
    if row_df[node.attr] <= node.thres:
        return predict(node.left, row_df)
    elif row_df[node.attr] > node.thres:
        return predict(node.right, row_df)


# Given a set of data, make a prediction for each instance using the Decision Tree
def test_predictions(root, df):

    num_correct = 0
    meta_list = []
    for i, v in enumerate(df['f_acid']):
        meta = {}
        for key in list(df.keys()):
            if key != 'quality':
                meta[key] = df[key][i]
        meta_list.append(meta)

    for i, row in enumerate(meta_list):
        prediction = predict(root, row)
        if 'quality' in df:
            if prediction == df['quality'][i]:
                num_correct += 1
        else:
            print(prediction)

    if 'quality' in df:
        print('Right prediction: ' + str(num_correct))
        print(float(num_correct) / len(df['quality']))


def main(trainFile, testFile, minleaf):
    # An example use of 'build_tree' and 'predict'
    fields, df_train = fwf_file_parse(trainFile, 'train')
    attributes = fields[0: -1]
    prediction_column = 'quality'
    root = build_tree(df_train, attributes, prediction_column, minleaf)
    fields, df_test = fwf_file_parse(testFile, 'test')

    test_predictions(root, df_train)
    test_predictions(root, df_test)


def slices(sentence):

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


def fwf_file_parse(file, type):
    
    data_dict = {}
    data = open(file)
    counter = 0
    fields = []
    for line in data:
    
        meta = list(slices(line))
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
    start_time = time.time()
    args = (sys.argv)

    trainFile = args[1]
    testFile = args[2]
    minleaf = args[3]

    main(trainFile, testFile, int(minleaf))
    #print("--- %s seconds ---" % (time.time() - start_time))
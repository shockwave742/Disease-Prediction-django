import logging
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
import graphviz
import random
import matplotlib.pyplot as plt



# TODO change the level
logging.basicConfig(filename='machineLearningModel.loging', level=logging.INFO)
import numpy as np


def makeTheTree():

    url = 'https://drive.google.com/file/d/1kvMs5zK1TRiUeg574_kbSc1mnWumDkxc/view?usp=sharing'
    file_id = url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id

    path = 'static\CSV\Training.csv'
    df_train = pd.read_csv(path, header=0)
    # df_train = pd.read_csv(dwn_url, header=0)
    # df_train.isna().sum().sum()

    df_train = df_train.fillna(0)
    df_train = df_train.drop(columns='Unnamed: 133')
    # logging.info(df_train.describe())
    # TODO why by 0 and not delte ?

    X = df_train.drop(columns=['prognosis'])
    y = df_train['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=44, shuffle=True)
    clf = tree.DecisionTreeClassifier(max_depth=50)
    clf = clf.fit(X_train, y_train)
    accuracy_train = accuracy_score(y_train, clf.predict(X_train))
    logging.info('Accuracy in validation: ', accuracy_train)
    print('Accuracy in validation: ', accuracy_train)
    #dot_data = tree.export_graphviz(clf, out_file='GraphicalTree.dot')
    #graph = graphviz.Source(dot_data)
    #graph.render("GraphicalTree")

    url = 'https://drive.google.com/file/d/1OVsjNHnIPjVn-IV4B-9brclk2xyNyoIE/view?usp=sharing'
    file_id = url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id

    path = 'static\CSV\Testing.csv'
    df_tests = pd.read_csv(path, header=0)
    # df_tests= pd.read_csv(dwn_url, header=0)
    # logging.info(df_tests.describe())
    # logging.info(df_train.isna().sum().sum())
    df_tests = df_tests.fillna(0)
    X_tests = df_tests.drop(columns=['prognosis'])
    y_tests = df_tests['prognosis']

    # taking log and saving it in a file
    accuracy_test = accuracy_score(y_tests, clf.predict(X_tests))
    logging.info('Accuracy in test: ', accuracy_test)
    print('Accuracy in test: ', accuracy_test)
    #logging.info('f1 Macro(Unweighted mean. This does not take label imbalance into account'
    #           '):', f1_score(y_tests, clf.predict(X_tests), average='macro'))
    #logging.info('recall score Macro: ', recall_score(y_tests, clf.predict(X_tests), average='macro'))

    return clf


def findDesesFromSymptom(Userinput):
    url = 'https://drive.google.com/file/d/1kvMs5zK1TRiUeg574_kbSc1mnWumDkxc/view?usp=sharing'
    file_id = url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id

    path = 'static\CSV\Training.csv'
    df_train = pd.read_csv(path, header=0)
    # df_train = pd.read_csv(dwn_url, header=0)
    # df_train.isna().sum().sum()

    df_train = df_train.fillna(0)
    df_train = df_train.drop(columns='Unnamed: 133')
    # logging.info(df_train.describe())
    # TODO why by 0 and not delte ?
    X = df_train.drop(columns=['prognosis'])
    final_input = pd.DataFrame(data=X, index=[1]).fillna(0)
    chose_symptom = Userinput.split(',')
    for i in chose_symptom:
        for column in final_input.columns:
            if i == column:
                final_input[column] = 1

    clf = makeTheTree()

    # we make a graphical tree of the clf
    tree.plot_tree(clf, filled=True)
    # and save it in a pdf file
    plt.savefig('graphicalTree.pdf')


    return clf.predict(final_input)  # returns disease
    # Might be helpful for test #


#print(findDesesFromSymptom('yellow_crust_ooze,palpitations'))


'''
l = {}
c = [1,0]
for a in range(132):
    b = random.choices([1,0],[1,3])
    l.update({str(a):b})
data =pd.DataFrame(data=l, index=[1])
logging.info(data)

logging.info(findDesesFromSymptom(data)[0])

logging.shutdown()
'''

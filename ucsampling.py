import pandas as pd
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import  SVC
import pickle as pk
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.stats import entropy
from utils import savePickle,getPicklefile,mapping,read_OnlyTrainData,read_OnlyTestData



def TrainInitialModelSample():

    train_data = read_OnlyTrainData(dropFileName=True);
    train_data = train_data[:20]

    X_train = train_data.drop('label',axis=1).values
    y_train = train_data['label']

    test_data = read_OnlyTestData(dropFileName=True,returnXy=False);
    X_test_set = test_data.drop('label', axis=1).values
    y_test_set = test_data['label']


    svmClassifier = SVC(C=10, kernel='linear', gamma=0.001, probability=True, random_state=500156)
    logRegClassifier = LogisticRegression(random_state=789)
    rfClassifier = RandomForestClassifier(criterion='entropy', random_state=4528)

    classifiers = {type(svmClassifier).__name__: svmClassifier,
                   type(logRegClassifier).__name__: logRegClassifier,
                   type(rfClassifier).__name__: rfClassifier,
                   }

    #Train all 3 classifires with initial data samlples

    experiments = []
    scores = {}
    for clfname,clf in classifiers.iteritems():

        clf.fit(X_train,y_train)
        y_pred = clf.predict(X_test_set)
        score = accuracy_score(y_pred,y_test_set)
        pred_probs = clf.predict_proba(X_test_set)

        modelObj = {}
        modelObj['classifier_name'] = clfname
        modelObj['acc_score'] = score
        modelObj['pred_probs'] = pred_probs
        modelObj['clf_obj'] = clf

        scores[clfname] = score
        #save models to pickle
        savePickle(clf,clfname)

        #print scores
        #save initial scores to pickle
        savePickle([scores[clfname]],clfname+'_scores')

        experiments.append(modelObj)

    return scores



















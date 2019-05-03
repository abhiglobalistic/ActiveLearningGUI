from scipy.stats import entropy
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from itertools import chain
import plotly
import json
import plotly.graph_objs as go
import itertools

from utils import getPicklefile, read_OnlyTestData,read_OnlyTrainData,savePickle,mapping

currentCount = 0

def updateGraph(scores):

    traces = []
    colors = {'LogisticRegression': 'rgb(31, 119, 180)',
              'SVC': 'rgb(255, 127, 14)',
              'RandomForestClassifier': 'rgb(44, 160, 44)'}

    for name,score in scores.iteritems():

        prev_scores = getPicklefile(name+'_scores')
        trace = go.Scatter(
            x=[j for j in range(0, 420, 20)],
            y=prev_scores,
            mode='lines+markers',
            name=name,
            line=dict(
                color=colors[name]
            ),
            showlegend=True
        )
        traces.append(trace)

    data = traces
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def generateOracleData(df_samples):

    oracleSamples = []
    savePickle(df_samples,'finalOracleSamples15')
    for df in df_samples:
        clfname = df['classifier'][0]
        for clip_name in df['sample']:
            instance = {'name': clip_name[-1], 'clip': 'static/datafiles/audiofiles/'+clip_name[-1]+'.mp3'}
            oracleSamples.append(instance)

    return oracleSamples

def setCurrentCount(value):
    global currentCount
    currentCount = value


def getCurrentCount():
    return currentCount


def computeOracle(stepSampleCount):

    # get test data of 50 instances
    X_test_set, y_test_set = read_OnlyTestData(dropFileName=True, returnXy=True)

    # get unlabelled samples total 430
    unlabelled_samples_data = read_OnlyTrainData(dropFileName=False)

    # get pickle files
    LogRegression = getPicklefile('LogisticRegression')
    RFClassifier = getPicklefile('RandomForestClassifier')
    Svc = getPicklefile('SVC')

    classifiers = {}
    classifiers[type(LogRegression).__name__] = LogRegression
    classifiers[type(RFClassifier).__name__] = RFClassifier
    classifiers[type(Svc).__name__] = Svc


    setCurrentCount(stepSampleCount)
    print ("COUNT",stepSampleCount)
    prevStepCount = 0
    if(stepSampleCount == 40):
        prevStepCount = 20
    else:
        prevStepCount = stepSampleCount - 20

    samples = unlabelled_samples_data[prevStepCount:stepSampleCount]
    samples_no_labels_song_name = samples.drop(['label','song name'], axis=1).values
    samples_with_songnames = samples.drop('label', axis=1).values


    scores = {}
    dfs = []
    for clfname, clf in classifiers.iteritems():
        # test accuracy on constant test set
        y_pred = clf.predict(X_test_set)
        score = accuracy_score(y_pred, y_test_set)
        # get probabilites on unlabelled samples for entropy
        pred_probs = clf.predict_proba(samples_no_labels_song_name)

        entropies_with_samples = []

        for indx in range(len(samples_no_labels_song_name)):
            entr = entropy(pred_probs[indx])
            withEntropy = [clfname,samples_with_songnames[indx], entr]
            entropies_with_samples.append(withEntropy)



        dataf = pd.DataFrame(columns=['classifier','sample', 'entropy'],data=entropies_with_samples)
        finalOracledf = dataf.sort_values(by='entropy',ascending=False)
        dfs.append(finalOracledf)


        scores[clfname] = score


    # save scores in pickle
    # for name, score in scores.iteritems():
    #     prev_scores = getPicklefile(name+"_scores")
    #     prev_scores.append(score)
    #     savePickle(prev_scores,name+'_scores')

    # update the graph with old scores and new scores


    # send samples to gui for labelling
    return generateOracleData(dfs)


def trainModels(trainingData):

    # get test data of 50 instances
    X_test_set, y_test_set = read_OnlyTestData(dropFileName=True, returnXy=True)

    # get pickle files
    LogRegression = getPicklefile('LogisticRegression')
    Svc = getPicklefile('SVC')
    RFClassifier = getPicklefile('RandomForestClassifier')

    classifiers = [LogRegression,Svc,RFClassifier]

    scores = {}
    for execNo in range(len(trainingData)):

        tdata = trainingData[execNo]
        tdata = mapping(tdata)
        X = tdata.drop(['label','audio_name'],axis=1).values
        y = tdata['label']

        clf = classifiers[execNo]
        clfname = type(clf).__name__

        # retrain the model
        clf.fit(X,y)
        y_pred = clf.predict(X_test_set)
        score = accuracy_score(y_pred, y_test_set)
        scores[clfname] = score
        # save models to pickle
        savePickle(clf, clfname)

        #get previous score and save it
        oldscores = getPicklefile(clfname+'_scores')

        oldscores.append(score)
        #print "OLD",oldscores
        # save scores to pickle
        savePickle(oldscores, clfname + '_scores')

    return scores



def train_withLabelledSamples(labelledSamples):

    finalOracleSamples15 = getPicklefile('finalOracleSamples15')

    addedLabelsDFs = []
    for inNum in range(len(finalOracleSamples15)):
        Modsamples = finalOracleSamples15[inNum]
        clfname = Modsamples['classifier'][0]
        labSamples = labelledSamples[inNum]
        for samp in labSamples:
            aname,value = samp.items()[0]
            for num in range(len(Modsamples['sample'])):
                if(aname in Modsamples['sample'][num]):
                    Modsamples.loc[num,'label'] = value

        Modsamples = Modsamples.replace(to_replace='None', value=np.nan).dropna()
        Modsamples = Modsamples.drop(['classifier', 'entropy'], axis=1).values

        flatArray = []
        for sample,label in Modsamples:
            sample = np.append(sample,label)
            flatArray.append(sample)

        trainingDF = pd.DataFrame(columns=['meanfreq', 'sd', 'median', 'Q25', 'Q75', 'IQR', 'skew', 'kurt', 'sp.ent',
                                           'sfm', 'mode', 'centroid', 'meanfun', 'minfun', 'maxfun',
                                           'meandom', 'mindom', 'maxdom',
                                           'dfrange', 'modindx', 'audio_name','label'],data=flatArray)

        addedLabelsDFs.append(trainingDF)


    # finally send data to models for training
    return trainModels(addedLabelsDFs)


























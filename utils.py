import pickle as pk
import pandas as pd


def mapping(dFrame):
    mapping = {'male': 1, 'female': 0}
    voiceData = dFrame.replace({'label': mapping})
    return voiceData


def read_OnlyTestData(dropFileName=True,returnXy=True):

    testVoiceData = pd.read_csv('static/datafiles/csvfiles/voice50_Test.csv')
    testVoiceData = mapping(testVoiceData)

    if (dropFileName == True):
        testVoiceData = testVoiceData.drop('song name', axis=1)

    X = testVoiceData.drop('label', axis=1).values
    y = testVoiceData['label']

    if(returnXy == True):
        return X,y
    else:
        return testVoiceData

def read_OnlyTrainData(dropFileName=True):

    trainVoiceData = pd.read_csv('static/datafiles/csvfiles/voice450_Train.csv')
    trainVoiceData = mapping(trainVoiceData)

    if(dropFileName == True):
        trainVoiceData = trainVoiceData.drop('song name',axis=1)
        return trainVoiceData
    else:
        return trainVoiceData


def savePickle(item,filename):
    pk.dump(item, open('static/datafiles/pickles/' + filename, 'wb'))
    print('Pickled file : {}'.format(filename) + ' saved !')

def getPicklefile(filename):
    modelfile = pk.load(open('static/datafiles/pickles/'+filename, 'rb'))
    return modelfile
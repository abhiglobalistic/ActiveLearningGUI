import os
from flask import Flask, render_template, request
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json
from flask_cors import CORS
import ucsampling
import compute
from utils import getPicklefile, savePickle


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True,static_url_path='/static')
    CORS(app)

    @app.route('/')
    def intialize():

        return render_template('index.html')


    app.add_url_rule('/', endpoint='index')


    @app.route('/graph')
    def line():
        scores = {}
        scores['LogisticRegression'] = 'lr'
        scores['RandomForestClassifier'] = 'rf'
        scores['SVC'] = 'svc'
        return compute.updateGraph(scores)



    @app.route('/getsamples',methods=['POST'])
    def getSamples_toAnnotate():
        constDiff = 20
        data = json.loads(request.data)
        runCount = int(data['stepSampleCount'])
        sampleCounter = runCount + constDiff
        if(sampleCounter == 420):
            return render_template('index.html')
        entropied_samples = compute.computeOracle(sampleCounter)

        logRegSample = entropied_samples[0:5]
        svmSample = entropied_samples[20:25]
        rfSample = entropied_samples[40:45]

        savePickle(logRegSample,'LogisticRegression_Samples')
        savePickle(svmSample, 'SVC_Samples')
        savePickle(rfSample, 'RandomForestClassifier_Samples')

        print (sampleCounter," samples")
        return json.dumps([logRegSample, svmSample, rfSample])




    @app.route('/train',methods=['POST'])
    def train_models():
        data = json.loads(request.data)
        labelled_data = np.array_split(data,3)
        scores = compute.train_withLabelledSamples(labelledSamples=labelled_data)


        return json.dumps(scores)

        #return json.dumps([logRegSample,svmSample,rfSample])



    @app.route('/onboot')
    def onboot():
        # run the initial Training of models
        scores = ucsampling.TrainInitialModelSample()
        return json.dumps(scores)


    @app.route('/currentCount')
    def getCurrentCount():
        return json.dumps(compute.getCurrentCount())



    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=False,threaded=True)
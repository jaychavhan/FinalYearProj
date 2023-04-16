
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from flask import Flask, render_template, request
import json

from legal_consequences import query

application = Flask(__name__)

# Define the AWS SageMaker endpoint name
# endpoint_name = 'Endpoint-Distilbert-Base-cased-1'

# Create a SageMaker runtime client
# sagemaker_runtime_client = boto3.client('runtime.sagemaker')


@application.route('/')
def home():
    return render_template('index.html')


@application.route('/classify', methods=['POST'])
def classify():
    # content_type = request.headers.get('Content-Type')
    # print(content_type)
    text = request.form.get('text')
    # # Send a request to the SageMaker endpoint to classify the text
    # response = sagemaker_runtime_client.invoke_endpoint(EndpointName=endpoint_name, Body=text.encode('utf-8'))
    # # Parse the response from the endpoint
    # result = json.loads(response['Body'].read().decode())
    # print(result)
    legal_consq = False
    highest_label = ''
    second_highest_label = ''
    third_highest_label = ''
    resultlist = []
    infolist = []
    output = query({
        "inputs": text,
    })
    for scoreList in output:
        highest_label = ''
        for dictitem in scoreList[:]:
            if dictitem['score'] < 0.5:
                scoreList.remove(dictitem)
        if len(scoreList) > 0:
            legal_consq = True
            resultlist.append('Legal Consequences')
            infolist.append('Posting this on social media might cause you legal consequences')
            highest_label = scoreList[0]['label']
        if len(scoreList) > 1:
            second_highest_label = scoreList[1]['label']
        if len(scoreList) > 2:
            third_highest_label = scoreList[2]['label']
    if legal_consq:
        list_of_labels = [highest_label, second_highest_label, third_highest_label]
        for item in list_of_labels:
            if item == 'identity_hate':
                resultlist.append('Communal violence')
                infolist.append('and It might spread communal hatred')
            if item == 'obscene':
                resultlist.append('Obscene Language')
                infolist.append('and It might damage reputations for using obscene language')
            if item == 'threat':
                resultlist.append('Threatening')
                infolist.append('and it sounds threatening')
            if item == 'insult':
                resultlist.append('Insulting')
                infolist.append('and it might insult someone or something')
            if item == 'toxic' or item == 'severe_toxic':
                resultlist.append('Toxicity')
                infolist.append('and it can spread toxicity')
        infolist.append('. Please Re-consider before posting or consult a lawyer')
        classification = ', '.join(resultlist)
        info = ' '.join(infolist)
    else:
        classification = 'No Legal Consequences'
        info = 'Safe to post'

    return render_template('index.html', text=text, classification=classification, info=info)


if __name__ == '__main__':
    application.run(debug=True)

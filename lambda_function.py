from slacker import Slacker
import botocore
from botocore.client import Config
import boto3
import json

def lambda_handler(event, context):

    if context == 'local':
        print "local Function logic Begins"
        # message = 'Slack Test from Adrian'
        message = getMessageFromLocalSNSEvent()
        token = getLocalSlackToken()
    else:
        print "Lambda Function Begins"
        message = getMessageFromSNSEvent(event)
        token = getS3SlackToken()

    slack = Slacker(token)

    # Send a message to #general channel...nope, use the slackapitest channel 
    # slack.chat.post_message('#slackapitest', 'Hello fellow Slackers and Study Gurus!')
    # message = 'Slack Test from Adrian'
    slack.chat.post_message('#slackapitest', message)

    # Get users list
    #response = slack.users.list()
    #users = response.body['members']
    # Upload a file
    #slack.files.upload('hello.txt')
    print "Function Complete"


def getLocalSlackToken():
    tokenFile = open("token.txt", "r")
    return tokenFile.readline()


def getMessageFromSNSEvent(event):
    messageInEvent = event['Records'][0]['Sns']['Message']
    # print('messageInEvent = '.format(messageInEvent))
    return messageInEvent


def getMessageFromLocalSNSEvent():
    SNSEventObject = {
        "Records": [
            {
              "EventVersion": "1.0",
              "EventSubscriptionArn": "arn:aws:sns:EXAMPLE",
              "EventSource": "aws:sns",
              "Sns": {
                "SignatureVersion": "1",
                "Timestamp": "1970-01-01T00:00:00.000Z",
                "Signature": "EXAMPLE",
                "SigningCertUrl": "EXAMPLE",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "Message": "Hello from local SNS! Object",
                "MessageAttributes": {
                  "Test": {
                    "Type": "String",
                    "Value": "TestString"
                  },
                  "TestBinary": {
                    "Type": "Binary",
                    "Value": "TestBinary"
                  }
                },
                "Type": "Notification",
                "UnsubscribeUrl": "EXAMPLE",
                "TopicArn": "arn:aws:sns:EXAMPLE",
                "Subject": "TestInvoke"
              }
            }
          ]
        }

    event = SNSEventObject
    # SNSEventFile = open("SNSEvent.txt", "r")
    # event_string = SNSEventFile.read().splitlines()
    # event = json.load(event_string)
    messageInEvent = event['Records'][0]['Sns']['Message']
    print('messageInEvent = {}'.format(messageInEvent))
    return messageInEvent


#Get file in S3 that contains API Key and return the first line which should be the key
def getS3SlackToken():
    #Check to see if file exists in the S3 bucket   
    s3resource = boto3.resource('s3', config=Config(signature_version='s3v4'))
    # s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    exists = False

    try:
        s3resource.Object('adrian-efiles-for-lambda', 'token.txt').load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            print 'There was an exception testing for file existence'
            print e
            raise e 
    else:
        exists = True
    # print('Does the file in AWS S3 exist?: {}'.format(exists))
    try:
        s3resource.meta.client.download_file('adrian-efiles-for-lambda', 'token.txt', '/tmp/token.txt')
    except Exception as e:
        print 'There was a problem accessing the file encrypted by AWS KMS'
        print e
        exit()

    tokenFile = open("/tmp/token.txt", "r")
    return tokenFile.readline()





# Call the the standard AWS Lambda Python handler function to begin
# Or call the program directly if testing outside of Lambda
if __name__ == '__main__':
    void_event = ''
    void_context = 'local'
    lambda_handler(void_event, void_context)

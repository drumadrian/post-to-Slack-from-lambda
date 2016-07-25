from slacker import Slacker

def lambda_handler(event, context):
    print "Function Begins"
    slack = Slacker('xoxp-46683194354-46684266002-54263070225-f31a395957')

    # Send a message to #general channel...nope, use the slackapitest channel 
    slack.chat.post_message('#slackapitest', 'Hello fellow slackers and now Ben!')

    # Get users list
    #response = slack.users.list()
    #users = response.body['members']

    # Upload a file
    #slack.files.upload('hello.txt')

    print "Function Complete"

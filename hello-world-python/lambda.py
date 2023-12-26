def lambda_handler(event, context):
    message = 'V1: Hello {} {}!'.format(event['first_name'], event['last_name'])
    return {
        'message' : message
    }

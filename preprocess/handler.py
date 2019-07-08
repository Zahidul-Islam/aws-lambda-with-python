import json
import string

translator = str.maketrans("", "", string.punctuation)


def process(event, context):
    """
    Makes text lower case, strips spaces, and removes punctuation.
    """
    body = json.loads(event['body'])
    text = body['text']
    text = text.lower().strip().replace("\n", " ").translate(translator)

    response = {
        "statusCode": 200,
        "body": json.dumps(text)
    }

    return response

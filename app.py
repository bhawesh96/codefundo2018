from flask import Flask, request
import json
import requests
import trains
from wit import Wit

app = Flask(__name__)

client = Wit('***REMOVED***')

page_token = 'EAAH4N0DZAmJQBAFlFauTRe0098BpCJQrwjniLDjZCVZBHTZCMxzjuvSZBlwVFehG6C1ai2NBfN9MgSpzoHzHrr75kS51WouqV8zjdV8duAvnUImNZCwlpZB2IIpvKvQ9t68KsxZAil8zF6B7Da8o1ExAFwlFvH8umgvBzZB6ZBnTLIDek8zlQo84rZB'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'codefundo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    print 'MSH TEXT: ' + message_text
                    print 'wit call now'

                    final_message = wit_parser(client.message(str(message_text)))

                    send_message(sender_id, final_message)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def wit_parser(resp):
    print 'resp from WIT'
    print ''
    print resp
    print ''
    for entity in resp['entities']:
        if(entity == 'travel_mode'):
            _travel_mode = resp['entities'][entity][0]['value']
            _source = resp['entities']['location'][0]['value']
            _destination = resp['entities']['location'][1]['value']
            if(_travel_mode == 'train'):
                return trains.train_between(_source, _destination, None), 200
    return "Sorry! I'm not smart enough yet!", 200


def send_message(recipient_id, message_text):

    params = {
        "access_token": page_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    
if __name__ == '__main__':
    app.run()
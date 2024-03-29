from flask import Flask, request
import json
import requests
import trains
import flights
import buses
import hotels
import translate
from wit import Wit
import time
import vision
import audio


app = Flask(__name__)

client = Wit('***REMOVED***')

page_token = 'Facebook_Page_Token'

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

                    if('text' in messaging_event["message"]):
                        message_text = messaging_event["message"]["text"]  # the message's text
                        # print 'MSG TEXT: ' + message_text
                        # print 'wit call now'

                        #final_message = wit_parser(client.message(str(message_text)))
                        #print str(final_message)
                        #send_message(sender_id, str(final_message))
                        send_message(sender_id, "Developers at work!\n Please check back later.\n Thanks!")


                    if('attachments' in messaging_event["message"]):
                        print 'attachment detected'
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]    
                        attach_type = messaging_event["message"]["attachments"][0]['type']
                        attach_url = messaging_event["message"]["attachments"][0]['payload']['url']
                        print str(attach_type)
                        print str(attach_url)
                        if(attach_type == 'image'):
                            # textx = str(vision.fetch(attach_url))
                            msg = "Result after IMAGE ANALYSIS is \n " + textx
                            # send_message(sender_id, msg)
                        if(attach_type == 'audio'):
                            # send_message(sender_id, 'received')
                            print 'now fetching'
                            # res = str(audio.download(attach_url))
                            # send_message(sender_id, res)
                            # res = str(audio.convert())
                            # send_message(sender_id, res)
                            # print 'now text conversion'
                            # res = str(audio.fetch())
                            # send_message(sender_id, res)
                            # final_message = wit_parser(client.message(str(res)))
                            # print str(final_message)
                            # send_message(sender_id, str(final_message))
                        send_message(sender_id, "Developers at work!\n Please check back later.\n Thanks!")


                if messaging_event.get("delivery"):  # delivery confirmatio
                    return '', 200

                if messaging_event.get("optin"):  # optin confirmation
                    return '', 200

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    return '', 200

    return "ok", 200

def wit_parser(resp):
    print 'resp from WIT'
    print ''
    print resp
    print ''
    try:
        for entity in resp['entities']:
            if(entity == 'phrase_to_translate'):
                _text = resp['entities']['phrase_to_translate'][0]['value']
                _lang = resp['_text'].split()[-1]
                return ("'" + str(_text) + "'" + ' in ' + str(_lang) + ' is => \n' +  str(translate.trans(_text, _lang)))
            elif(entity == 'hotel'):
                _destination = resp['entities']['location'][0]['value']
                return hotels.hotel_in(_destination)
            elif(entity == 'pnr'):
                _pnr = resp['entities']['number'][0]['value']
                return trains.pnr_status(_pnr)
            elif(entity == 'live_status'):
                _train_num = resp['entities']['number'][0]['value']
                return trains.live_train_status(_train_num)
            elif(entity == 'travel_mode'):
                date=None
                if('datetime' in resp['entities']):
                    _date = resp['entities']['datetime'][0]['values'][0]['value']
                    date = (str(_date)[0:10].replace('-',''))
                _travel_mode = resp['entities'][entity][0]['value']
                _source = resp['entities']['location'][0]['value']
                _destination = resp['entities']['location'][1]['value']
                if(_travel_mode == 'train'):
                    return trains.train_between(_source, _destination, date)
                elif(_travel_mode == 'bus'):
                    return buses.bus_between(_source, _destination, date)
                elif(_travel_mode == 'flight'):
                    _adults = '1'
                    if('number' in resp['entities']):
                        _adults = resp['entities']['number'][0]['value']
                    return flights.flight_between(_source, _destination, date, _adults)
                
    except Exception as e:
        return 'app.py error: ' + str(e)
    return "Sorry! I'm not smart enough yet!"


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
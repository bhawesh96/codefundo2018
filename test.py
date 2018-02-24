from wit import Wit
import trains

client = Wit('***REMOVED***')

resp = client.message('live status of train 12859')

def wit_parser(resp):
    for entity in resp['entities']:
    	print resp
    	if(entity == 'live_status'):
    		_train_num = resp['entities']['number'][0]['value']
        	return trains.live_train_status(_train_num)
        elif(entity == 'travel_mode'):
            _travel_mode = resp['entities'][entity][0]['value']
            _source = resp['entities']['location'][0]['value']
            _destination = resp['entities']['location'][1]['value']
            if(_travel_mode == 'train'):
            	print _source
            	print _destination
                return trains.train_between(_source, _destination, None) 
    return "Sorry! I'm not smart enough yet"

print wit_parser(resp)
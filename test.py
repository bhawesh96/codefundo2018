from wit import Wit

client = Wit('***REMOVED***')

resp = client.message('train from Mumbai to Udupi')
print str(resp)

def wit_parser(resp):
    for entity in resp['entities']:
        if(entity == 'travel_mode'):
            _travel_mode = resp['entities'][entity][0]['value']
            _source = resp['entities']['location'][0]['value']
            _destination = resp['entities']['location'][1]['value']
            if(_travel_mode == 'train'):
                return trains.train_between(f_station, t_station, None)
    return "Sorry! I'm not smart enough yet"

import trains
print (trains.train_between('Mumbai', 'Udupi', None))
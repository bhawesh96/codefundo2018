from wit import Wit
import trains
import flights, requests, json
import datetime
import buses
import translate

base_url="http://developer.goibibo.com/api/search/?app_id=b2f41b4c&app_key=<app_key>&format=json&"

client = Wit('***REMOVED***')

resp = client.message('flight from mumbai to pune 4 tickets')

def wit_parser(resp):
    print 'resp from WIT'
    print ''
    print resp
    print ''
    for entity in resp['entities']:
        if(entity == 'phrase_to_translate'):
            _text = resp['entities']['phrase_to_translate'][0]['value']
            _lang = resp['_text'].split()[-1]
            return str(translate.trans(_text, _lang))
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
            _travel_mode = resp['entities'][entity][0]['value']
            _source = resp['entities']['location'][0]['value']
            _destination = resp['entities']['location'][1]['value']
            if(_travel_mode == 'train'):
                return trains.train_between(_source, _destination, None)
            elif(_travel_mode == 'bus'):
                return buses.bus_between(_source, _destination,'20180225')
            elif(_travel_mode == 'flight'):
                _adults = '1'
                if('number' in resp['entities']):
                    _adults = resp['entities']['number'][0]['value']
                return flights.flight_between(_source, _destination,'20180225', _adults)

print wit_parser(resp)
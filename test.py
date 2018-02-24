from wit import Wit
import trains
import flights
import datetime

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

def flight_between(src,dest,date,adults,cl='E',show_min=False,children="0",infants="0"):
	if(not date):
		date=str(datetime.datetime.today().strftime('%Y%m%d'))
	code_src = (flights.get_airport_code(src))
	code_dest = (flights.get_airport_code(dest))
	c = cl.upper()
	ad = str(adults)
	child = children
	infant = infants
	url = base_url+"source="+code_src+"&destination="+code_dest+"&dateofdeparture="+date+"&seatingclass="+c+"&adults="+ad+"&children="+child+"&infants="+infant+"&counter=100"
	response = requests.get(url)
	data = response.json()
	data = data["data"]["onwardflights"]

	m = 100000
	res = ""
	for j,row in enumerate(data):
		res=res+"Origin:"+row["origin"]+"\n"
		res=res+"Destination:"+row["destination"]+"\n"
		res=res+"Departure time:"+row["deptime"]+"\n"
		res=res+"Arrival Time:"+row["arrtime"]+"\n"
		res+="Travel Time:"+row["duration"]+"\n"
		res+="Airline:"+row["airline"]+"\n"
		if(row["seatsavailable"]>"300"):
			res+="Seats Available:"+"NA"+"\n"
		else:
			res+="Seats:"+row["seatsavailable"]+"\n"
		res+="Fare:"+str(row["fare"]["grossamount"])+"\n"
		if row["fare"]["grossamount"]<=m:
			m=row["fare"]["grossamount"]
			pos = j
		if row["destination"]!=code_dest:
			res+="Onward Source:"+row["onwardflights"][0]["origin"]+"\n"
			res+="Destination:"+row["onwardflights"][0]["destination"]+"\n"
			res+="Departure time:"+row["onwardflights"][0]["deptime"]+"\n"
			res+="Onward Airline:"+row["onwardflights"][0]["airline"]+"\n"
		res=res+"\n"

	if show_min==True:
		min_airline=""
		min_airline+="Origin:"+data[pos]["origin"]+"\n"
		min_airline+= "Destination:"+data[pos]["destination"]+"\n"
		min_airline+="Departure time:"+data[pos]["deptime"]+"\n"
		min_airline+= "Arrival Time:"+data[pos]["arrtime"]+"\n"
		min_airline+="Travel Time:"+data[pos]["duration"]+"\n"
		min_airline+="Airline:"+data[pos]["airline"]+"\n"
		if(data[pos]["seatsavailable"]>"300"):
			min_airline+="Seats Available:"+"NA"+"\n"
		else:
			min_airline+="Seats:"+data[pos]["seatsavailable"]+"\n"		
		min_airline+="Fare:"+str(data[pos]["fare"]["grossamount"])+"\n"
		return min_airline
	else:
		return res

print flight_between("mumbai","mangalore","20180301", '4')
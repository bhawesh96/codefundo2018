import requests
import json
import datetime

app_id="b2f41b4c"
api_key="***REMOVED***"
base_url="http://developer.goibibo.com/api/bus/search/?app_id=b2f41b4c&app_key=***REMOVED***&format=json&"

def bus_between(src,dest,date):
	if(not date):
		date=str(datetime.datetime.today().strftime('%Y%m%d'))
	url=base_url+"source="+src+"&destination="+dest+"&dateofdeparture="+date
	response = requests.get(url)
	data = response.json()
	data = data["data"]["onwardflights"]
	res=""
	i=0
	for row in data:
		res+="Origin:"+row["origin"]+"\n"
		res+="Destination:"+row["destination"]+"\n"
		res+="Departure Time:"+row["DepartureTime"]+"\n"
		res+="Arrival Time:"+row["ArrivalTime"]+"\n"
		res+="Seat:"+row["seat"]+"\n"
		res+="Duration:"+row["duration"]+"\n"
		res+="Type:"+row["BusType"]+"\n"
		res+="Fare:"+row["fare"]["totalfare"]+"\n"
		res+="Travels Name"+row["TravelsName"]+"\n"
		res+="\n"
		i=i+1
		if i==7:
			break
	return str(res)

def filter1(src,dest,date,filter):
	if(not date):
		date=str(datetime.datetime.today().strftime('%Y%m%d'))
	url=base_url+"source="+src+"&destination="+dest+"&dateofdeparture="+date
	response = requests.get(url)
	data = response.json()
	data = data["data"]["onwardflights"]
	res=""
	i=0
	for row in data:
		if(filter in row["seat"]):
			res+="Origin:"+row["origin"]+"\n"
			res+="Destination:"+row["destination"]+"\n"
			res+="Departure Time:"+row["DepartureTime"]+"\n"
			res+="Arrival Time:"+row["ArrivalTime"]+"\n"
			res+="Seat:"+row["seat"]+"\n"
			res+="Duration:"+row["duration"]+"\n"
			res+="Type:"+row["BusType"]+"\n"
			res+="Fare:"+row["fare"]["totalfare"]+"\n"
			res+="Travels Name:"+row["TravelsName"]+"\n"
			res+="\n"
			i=i+1
			if i==7:
				break
	return str(res)


# seat_type_filter = "ST"
# result = filter1("bangalore","mangalore","20180301",seat_type_filter)
# print(result)
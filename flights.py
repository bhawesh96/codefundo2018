import requests
import json
import datetime

app_id="b2f41b4c"
api_key="<app_key>"
base_url="http://developer.goibibo.com/api/search/?app_id=b2f41b4c&app_key=<app_key>&format=json&"

def get_airport_code(city):
	f=open("IATADatabase.py")
	text = f.read()
	city = city.strip().lower().title()
	code=""
	l = text.split(' ')
	i=0
	for word in l:
		word = word.replace(",", "")
		word = word.replace("'","")
		if(word==city):
			i=999;
		if i==997:
			code=word
			break
		i=i-1
	return (code)

def flight_between(src,dest,date,adults,cl='E',show_min=False,children="0",infants="0"):
	if(not date):
		date=str(datetime.datetime.today().strftime('%Y%m%d'))
	print date
	code_src = (get_airport_code(src))
	code_dest = (get_airport_code(dest))
	c = 'E'
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
		return str(min_airline)
	else:
		return str(res)


# result = flight_between("mumbai","mangalore","20180225",'4')
# result = get_airport_code("mumbai")
# print(type(result))
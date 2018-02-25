from urlparse import urlparse
import requests
import urllib

def trans(text, t_l):
	subscriptionKey = '<subscription_key>'

	path = 'http://api.microsofttranslator.com/V2/Http.svc/Translate'
	t_l.lower()
	if(t_l=="german"):
		target ='de'
	elif(t_l=="english"):
		target= 'en-us'
	elif(t_l=="chinese"):
		target='zh-CHS'
	elif(t_l=="spanish"):
		target='es'
	elif(t_l=="french"):
		target='fr'

	params = '?to=' + target + '&text=' + urllib.pathname2url(text)

	def get_suggestions ():
	    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
	    r = requests.get(path+params, headers=headers)
	    return r.text

	result = get_suggestions ()
	z = result.encode('ascii', 'ignore').decode('ascii')
	z=z[68: len(z)-9]
	return(str(z))
# print(trans("My  name is Diptark", "french"))
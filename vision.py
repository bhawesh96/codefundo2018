import requests, json

features = [
    {
      "type":"TEXT_DETECTION",
      "maxResults":3
    }
]


def fetch(img_url):
    body = {
      "requests":[
        {
          "image":{
            "source":{
              "imageUri": img_url
            }
          },
          "features": features
        }
      ]
    }
    api = 'https://vision.googleapis.com/v1/images:annotate?key=<key>'
    r = requests.post(api, data=json.dumps(body))
    desc = json.loads(r.text)['responses'][0]['textAnnotations'][0]['description']
    return str(desc)
'''
def parse(r):
    resp = json.loads(r)
    dictx = resp['responses'][0]
    logoAnnotations = {'desc':None, 'score':None}
    landmarkAnnotations = {'landmark':None, 'score':None, 'latitude':None, 'longitude':None}
    
    final_dict = {}

    if('logoAnnotations' in dictx):
      logoAnnotations['score'] = dictx['logoAnnotations'][0]['score']
      logoAnnotations['desc'] = dictx['logoAnnotations'][0]['description']
      # print logoAnnotations

    if('landmarkAnnotations' in dictx):
      landmarkAnnotations['landmark'] = dictx['landmarkAnnotations'][0]['description']
      landmarkAnnotations['score'] = dictx['landmarkAnnotations'][0]['score']
      landmarkAnnotations['latitude'] = dictx['landmarkAnnotations'][0]['locations'][0]['latLng']['latitude']
      landmarkAnnotations['longitude'] = dictx['landmarkAnnotations'][0]['locations'][0]['latLng']['longitude']
      # print landmarkAnnotations

    if('webDetection' in dictx):
      webDesc = []
      bestGuessLabel = []
      for entity in dictx['webDetection']['webEntities']:
        webDesc.append(entity['description'])
      for label in dictx['webDetection']['bestGuessLabels']:
        bestGuessLabel.append(label['label'])
      # print bestGuessLabel
      # print desc
      
    if('labelAnnotations' in dictx):
      labels = []
      for label in dictx['labelAnnotations']:
        labels.append(label['description'])
      # print labels

    if('textAnnotations' in dictx):
      textx = ''
      for text in dictx['textAnnotations']:
        textx = textx + text
      print textx

    final_dict['logoDesc'] = logoAnnotations['desc']
    final_dict['lat'] = landmarkAnnotations['latitude']
    final_dict['long'] = landmarkAnnotations['longitude']
    final_dict['landmark'] = landmarkAnnotations['landmark']
    final_dict['webDesc'] = webDesc
    final_dict['bestGuessLabel'] = bestGuessLabel
    final_dict['label'] = labels
    return json.dumps(final_dict)
'''
import requests, json
import os, io, base64

import urllib

def fetch(img_url):
    urllib.urlretrieve(img_url, "my_image.jpg")
    file_name = os.path.join(
    os.path.dirname(__file__),
    'my_image.jpg')

    with io.open(file_name, 'rb') as image_file:
        # content = image_file.read()
        content = base64.b64encode(image_file.read())
    body = {
      "requests":[
        {
          "image":{
            "content":content
          },
          "features":[
            {
              "type":"TEXT_DETECTION",
              "maxResults":2
            }
          ]
        }
      ]
    }
    api = 'https://vision.googleapis.com/v1/images:annotate?key=<key>'
    r = requests.post(api, data=json.dumps(body))
    desc = json.loads(r.text)['responses'][0]['textAnnotations'][0]['description']
    return str(desc)

# print fetch('https://scontent-ort2-1.xx.fbcdn.net/v/t34.0-12/28381721_1806404329410148_930903050_n.jpg?_nc_ad=z-m&_nc_cid=0&oh=4e8b4b2aed3aeea5fcfec49ebc84541d&oe=5A946586')
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
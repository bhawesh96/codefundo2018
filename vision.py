import requests, json
import os, io, base64

import urllib

def text_generator(dic):
    web =''
    label=''
    bestGuessLabel=''
    logo=''
    gps=''
    landmark=''
    text=''

    try:
        if(len(dic['webDesc']) > 1):
            web_desc = ''
            webHeading = "Following are the Web Detected keypoints : \n"
            for ele in dic['webDesc']:
                web_desc = web_desc + ele + '\n'
            web = webHeading + web_desc
        if(len(dic['label']) > 1):
            label_desc = ''
            labelHeading = "Following are the some other relevant labels : \n"
            for ele in dic['label']:
                label_desc = label_desc + ele + '\n'
            label = labelHeading + label_desc
        if(len(dic['bestGuessLabel']) > 0):
            bestGuessLabelHeading = "The Best Guess we could make is : \n"
            for ele in dic['bestGuessLabel']:
                bestGuessLabel_desc = ele + '\n'
            bestGuessLabel = bestGuessLabelHeading + bestGuessLabel_desc
        if(dic['logoDesc']!=None):
            logoHeading = "We found the logo of : \n"
            logo_desc = dic['logoDesc'] + '\n'
            logo = logoHeading + logo_desc
        if(dic['lat']!=None and dic['long']!=None):
            gpsHeading = "We found the GPS coordinates of this image to be : \n"
            gps_desc = str(dic['lat']) + ' , ' + str(dic['long'])
            gps = gpsHeading + gps_desc
        if(dic['landmark']):
            landmarkHeading = "We found the landmark of the image as : \n"
            landmark_desc = dic['landmark'] + '\n'
            landmark = landmarkHeading + landmark_desc
        if(len(dic['textDesc']) > 1):
            textHeading = "We scraped the image text as : \n"
            text_desc = dic['textDesc'] + '\n'
            text = textHeading + text_desc
        return str((web + '\n' + label + '\n' + bestGuessLabel + '\n' + logo + '\n' + gps + '\n' + landmark + '\n' + text))
    except Exception as e:
        return str(e)


def parser(r):
    resp = json.loads(r)
    dictx = resp['responses'][0]
    textx = ''
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
      if('webEntities' in dictx['webDetection']):
        for entity in dictx['webDetection']['webEntities']:
          webDesc.append(entity['description'])
      if('bestGuessLabels' in dictx['webDetection']):
        if('label' in dictx['webDetection']['bestGuessLabels'][0]):
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
      textx = dictx['textAnnotations'][0]['description']

    final_dict['textDesc'] = textx
    final_dict['logoDesc'] = logoAnnotations['desc']
    final_dict['lat'] = landmarkAnnotations['latitude']
    final_dict['long'] = landmarkAnnotations['longitude']
    final_dict['landmark'] = landmarkAnnotations['landmark']
    final_dict['webDesc'] = webDesc
    final_dict['bestGuessLabel'] = bestGuessLabel
    final_dict['label'] = labels
    return text_generator(final_dict)


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
              "type":"WEB_DETECTION",
              "maxResults":5
            },
            {
              "type":"LABEL_DETECTION",
              "maxResults":5
            },
            {
              "type":"LANDMARK_DETECTION",
              "maxResults":2
            },
            {
              "type":"LOGO_DETECTION",
              "maxResults":1
            },
            {
              "type":"TEXT_DETECTION",
              "maxResults":3
            }
          ]
        }
      ]
    }
    api = 'https://vision.googleapis.com/v1/images:annotate?key=<key>'
    r = requests.post(api, data=json.dumps(body))
    # desc = json.loads(r.text)['responses'][0]['textAnnotations'][0]['description']
    print (r.text).encode('utf8')
    return parser(r.text)

# print fetch('https://scontent-ort2-1.xx.fbcdn.net/v/t34.0-12/28381721_1806404329410148_930903050_n.jpg?_nc_ad=z-m&_nc_cid=0&oh=4e8b4b2aed3aeea5fcfec49ebc84541d&oe=5A946586')

# print fetch('https://scontent-ort2-1.xx.fbcdn.net/v/t35.0-12/28418504_1806411499409431_82324897_o.jpg?_nc_ad=z-m&_nc_cid=0&oh=79365c88be0d5335b6a0a71d41539c54&oe=5A945ABF')
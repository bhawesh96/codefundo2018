x = {
  "responses": [
    {
      "labelAnnotations": [
        {
          "mid": "/m/05wrt",
          "description": "property",
          "score": 0.8757976,
          "topicality": 0.8757976
        },
        {
          "mid": "/m/020ys5",
          "description": "condominium",
          "score": 0.6605888,
          "topicality": 0.6605888
        },
        {
          "mid": "/m/023907r",
          "description": "real estate",
          "score": 0.6327176,
          "topicality": 0.6327176
        },
        {
          "mid": "/m/05s2s",
          "description": "plant",
          "score": 0.582637,
          "topicality": 0.582637
        },
        {
          "mid": "/m/01x314",
          "description": "facade",
          "score": 0.568249,
          "topicality": 0.568249
        }
      ],
      "webDetection": {
        "webEntities": [
          {
            "entityId": "/m/09c6w",
            "score": 2.6432,
            "description": "Hyderabad"
          },
          {
            "entityId": "/m/04sv4",
            "score": 0.8343,
            "description": "Microsoft"
          },
          {
            "entityId": "/m/0drzplk",
            "score": 0.7054,
            "description": "Microsoft Office 365"
          },
          {
            "entityId": "/m/052zb",
            "score": 0.7033,
            "description": "Microsoft Office"
          },
          {
            "entityId": "/m/09ggqdp",
            "score": 0.6997,
            "description": "Microsoft India"
          }
        ],
        "bestGuessLabels": [
          {
            "label": "microsoft office hyderabad",
            "languageCode": "en"
          }
        ]
      }
    }
  ]
}


dictx = x

for ele in dictx['responses'][0]['webDetection']:
  print ele






if('webEntities' in dictx['webDetection']):
  for entity in dictx['webDetection']['webEntities']:
    webDesc.append(entity['description'])
if('bestGuessLabels' in dictx['webDetection']):
  if('label' in dictx['webDetection']['bestGuessLabels']):
    for label in dictx['webDetection']['bestGuessLabels']:
      bestGuessLabel.append(label['label'])

print bestGuessLabel
print webDesc
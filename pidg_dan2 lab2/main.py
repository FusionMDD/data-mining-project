import tweepy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
import urllib.request
from geopy.geocoders import Nominatim

def b64_utf_8(file_contents):
   return base64.b64encode(file_contents).decode('UTF-8')

def query_labels(image_content):
   # побудова запиту
   service_request = service.images().annotate(body={
       'requests': [{
           'image': {
               'content': image_content
           },
           'features': [{
               'type': 'LABEL_DETECTION',
               'maxResults': 5
           }]
       }]
   })
   # виклик API
   service_response = service_request.execute()
   # обробка відповіді
   labels = [{'label': r['description'], 'score': r['score']} for r in
             service_response['responses'][0]['labelAnnotations']]
   return labels

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)
client = language.LanguageServiceClient()
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
a=input('latitude ')
a+=','
b=input('longtitude ')
bs=b;
b+=','
c=input('range ')
auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
geolocator = Nominatim()

for tweet in tweepy.Cursor(api.search,q="*",lang="en",filter="images",geo_enabled="true",count=100,geocode=a+b+c).items(100):
    print([tweet.text.encode('utf-8')])
    text = tweet.text.encode('utf-8')
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    try:
        url_response = urllib.request.urlopen(tweet.entities['media'][0]['media_url'])
        image = query_labels(b64_utf_8(url_response.read()))
        print(image)
    except (NameError, KeyError):
        pass

        location = geolocator.reverse(a+bs)
        print(location)

    print()
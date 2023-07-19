from requests_oauthlib import OAuth1Session
import os
import json
import sys, getopt

tokenFile = ''
dataText = ''
verbose = False
opts, args = getopt.getopt(sys.argv[1:],"ha:d:v",["access=","data=","verbose"])
for opt, arg in opts:
      if opt == '-h':
         print ('test.py -d <data text> -a <tokens file> -v verbose ')
         sys.exit()
      elif opt in ("-a", "--access"):
         tokenFile = arg
      elif opt in ("-d", "--data"):
         dataText = arg
      elif opt in ("-v", "--verbose"):
         verbose = True
 
if verbose == True:
  print ('Authorization file is ', tokenFile)
  print ('Data text is ', dataText)


# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
payload = {"text": dataText}


#print(oauth_tokens)
#print("Got access token: %s" % access_token)
#print("Got access token secret: %s" % access_token_secret)

# reading the access token data from the file
with open(tokenFile) as f:
    data = json.load(f)
  
#print("Data type before reconstruction : ", type(data))
if verbose == True:
  print(data)
      
access_token = data["oauth_token"]
access_token_secret = data["oauth_token_secret"]

print("Loaded access token: %s" % access_token)
print("Loaded access token secret: %s" % access_token_secret)

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)



# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))






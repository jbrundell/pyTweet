from requests_oauthlib import OAuth1Session
import os
import json
import sys, getopt

tokenFile = 'accessTokens.txt'
verbose = False
opts, args = getopt.getopt(sys.argv[1:],"ha:d:v",["access=","verbose"])
for opt, arg in opts:
      if opt == '-h':
         print ('test.py -a <tokens file> -v verbose ')
         sys.exit()
      elif opt in ("-a", "--access"):
         tokenFile = arg
      elif opt in ("-v", "--verbose"):
         verbose = True


# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")


# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)
print("Got OAuth token secret: %s" % resource_owner_secret)



# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)

# Fix Python 2.x.
try: input = raw_input
except NameError: pass
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

#print(oauth_tokens)
if verbose == True:
  print(json.dumps(oauth_tokens))

print("Got access token: %s" % access_token)
print("Got access token secret: %s" % access_token_secret)

print("Writing tokens to: ", tokenFile)
with open(tokenFile, 'w') as f:
    f.write(json.dumps(oauth_tokens))

#exit()






from krunker_api import krunker_api
import json

data = krunker_api("goonmandu")
json_string = json.dumps(data)
print(json_string)

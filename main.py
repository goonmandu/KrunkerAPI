from krunker_api import krunker_api
import json

data = krunker_api("x", debug=True)
json_string = json.dumps(data)
print(json_string)

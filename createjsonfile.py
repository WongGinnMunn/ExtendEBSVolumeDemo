import json

def script_handler(events, context):
  my_dict = {
    "InstanceId": events["InstanceId"]
  }
  
  json_string = json.dumps(my_dict, indent=2)
  with open('temp.json', 'w') as f:
    f.write(json_string)

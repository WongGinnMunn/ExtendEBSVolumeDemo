import json

my_dict = {
  "people": [
    {
      "name": "Bob",
      "age": 28
    }
  ]
}

json_string = json.dumps(my_dict)
with open('hello.json', 'w') as f:
  f.write(json_string)

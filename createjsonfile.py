import json
import sys
def main(events):
  my_dict = {
          "InstanceId": events[0]
  }

  json_string = json.dumps(my_dict, indent=2)
  with open('temp.json', 'w') as f:
    f.write(json_string)


if __name__ == '__main__':
  main(sys.argv[1:])

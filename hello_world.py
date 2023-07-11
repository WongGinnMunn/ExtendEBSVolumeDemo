import sys
import json

def main(event):
  f = open('InstanceData.json')
  data = json.load(f)
  print(data['InstanceId'])

if __name__ == '__main__':
    main(sys.argv[1:])

import sys
import json

def main(event):
  f = open('InstanceData.json')
  data = json.load(f)
  for i in data['InstanceId']:
    print(i)

if __name__ == '__main__':
    main(sys.argv[1:])

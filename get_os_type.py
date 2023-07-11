import boto3
import json
import sys

ssm_client = boto3.client("ssm", 'us-east-1')

def main(arg):
    with open("InstanceData.json",'r+') as file:
          # First we load existing data into a dict.
        event = json.load(file)
    
    try:
        instance_info = ssm_client.describe_instance_information(
            InstanceInformationFilterList=[
                {"key": "InstanceIds",
                    "valueSet": [event['InstanceId']]}
            ]
        )
        print("hello2")
        if len(instance_info["InstanceInformationList"]) > 0:
            os_type = instance_info["InstanceInformationList"][0]["PlatformType"]
            
            event.append({"OS_type":os_type})
            file.seek(0)
            json.dump(event, file, indent = 4)

            return arg
        else:
            raise Exception(
                "Please give permission to Systems Manager")
    except Exception as e:
        raise Exception(e)

if __name__ == '__main__':
  main(sys.argv[1:])

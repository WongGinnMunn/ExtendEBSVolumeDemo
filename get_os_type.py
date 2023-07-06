import boto3
import json
import sys

ssm_client = boto3.client("ssm", 'us-east-1')

def main(event):
    print("hello1")
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
            event['OS_type'] = os_type
            print("hello3")
            return event
        else:
            print("hello4")
            raise Exception(
                "Please give permission to Systems Manager")
    except Exception as e:
        print("hello5")
        raise Exception(e)

if __name__ == '__main__':
  data=json.loads(sys.argv[1])
  main(data)

'''
{
  "InstanceId": "i-0d048bb574834bfa1",
  "OS_type": "Linux"
}
'''

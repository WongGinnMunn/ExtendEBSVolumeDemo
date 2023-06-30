import boto3
import json

ssm_client = boto3.client("ssm")

def main(event):
    try:
        instance_info = ssm_client.describe_instance_information(
            InstanceInformationFilterList=[
                {"key": "InstanceIds",
                    "valueSet": [event['InstanceId']]}
            ]
        )
        if len(instance_info["InstanceInformationList"]) > 0:
            os_type = instance_info["InstanceInformationList"][0]["PlatformType"]
            event['OS_type'] = os_type
            return event
        else:
            raise Exception(
                "Please give permission to Systems Manager")
    except Exception as e:
        raise Exception(e)



'''
{
  "InstanceId": "i-0d048bb574834bfa1",
  "OS_type": "Linux"
}
'''

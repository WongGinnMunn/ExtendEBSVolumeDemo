import boto3
import json
import sys

ssm_client = boto3.client("ssm", 'us-east-1')

def main(arg):
    with open('InstanceData.json','r+') as file:

        file_data = json.load(file)
        
        try:
            instance_info = ssm_client.describe_instance_information(
                InstanceInformationFilterList=[
                    {"key": "InstanceIds",
                        "valueSet": [file_data['InstanceId']]}
                ]
            )

            if len(instance_info["InstanceInformationList"]) > 0:
                os_type = instance_info["InstanceInformationList"][0]["PlatformType"]
                
                toAppend = {"OS_Type": os_type}
                file_data.append(toAppend)
                file.seek(0)
                json.dump(file_data, file, indent = 4)

                return arg
            
            else:
                raise Exception(
                    "Please give permission to Systems Manager")
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
  main(sys.argv[1:])

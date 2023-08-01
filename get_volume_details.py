import json
import sys
import boto3
import math

ec2 = boto3.client('ec2', 'ap-southeast-1')


def getVolumeId(instance_id):
    response = ec2.describe_instance_attribute(
        InstanceId=instance_id, Attribute='blockDeviceMapping')
    res = response["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]
    return res


def getVolumeSize(volume_id):
    response = ec2.describe_volumes(
        VolumeIds=[
            volume_id
        ]
    )
    return response['Volumes'][0]['Size']


def newVolumeSize(size):
    return math.ceil(size*1.2)


def main(arg):
    with open('InstanceData.json', 'r+') as file:

        file_data = json.load(file)
        
        volumeId = getVolumeId(file_data['InstanceId'])
        current_size = getVolumeSize(volumeId)
        
        toAppend = {
            "VolumeId": volumeId,
            "OldSize": str(current_size),
            "NewSizeGib": str(newVolumeSize(current_size))
        }
        
        file_data.update(toAppend)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        
        return arg


if __name__ == '__main__':
    main(sys.argv[1:])


'''
{
  "InstanceId": "i-0d048bb574834bfa1",
  "OS_type": "Linux"
  "VolumeId": "vol-096e916cf93e76ef7",
  "OldSize": "10",
  "NewSizeGib": "12"
}
'''

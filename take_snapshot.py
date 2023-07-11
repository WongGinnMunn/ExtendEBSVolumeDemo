import json
import sys
import boto3

ec2 = boto3.client('ec2', 'us-east-1')


def main(arg):
    with open('InstanceData.json', 'r+') as file:
        file_data = json.load(file)
        
        try:
            response = ec2.create_snapshot(
                Description="a snapshot before the volume resizing",
                VolumeId=file_data["VolumeId"]
            )

            toAppend = {"SnapshotId": response["SnapshotId"]}
            
            file_data.update(toAppend)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            
            return arg
        except Exception as e:
            raise Exception(e)
    
    
if __name__ == '__main__':
    main(sys.argv[1:])



    #  include ec2: create tags permission

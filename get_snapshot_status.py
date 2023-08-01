import json
import sys
import boto3

ec2_client = boto3.client('ec2', 'ap-southeast-1')


def main(arg):
    with open('InstanceData.json', 'r+') as file:
        file_data = json.load(file)
        
        response = ec2_client.describe_snapshots(
            SnapshotIds=[
                file_data['SnapshotId']
            ],
        )
        while (response['Snapshots'][0]['State'] != 'completed'):

            response = ec2_client.describe_snapshots(
                SnapshotIds=[
                    file_data['SnapshotId']
                ],
            )
        
        toAppend = {"Snapshot_Status": response['Snapshots'][0]['State']}
        
        file_data.update(toAppend)
        file.seek(0)
        json.dump(file_data, file, indent=4)
            
            
        return arg


if __name__ == '__main__':
    main(sys.argv[1:])

import json
import boto3

ec2_client = boto3.client('ec2', 'us-east-1')

'''

Purpose:
    Delete snapshot after extending the volume. 


'''

def main():
    with open('InstanceData.json', 'r+') as file:
        file_data = json.load(file)
        
        try:
            response = ec2_client.delete_snapshot(
                SnapshotId=file_data["SnapshotId"]
            )

        except Exception as e:
            raise Exception(e)
    
    
if __name__ == '__main__':
    main()

import json
import boto3
import time

ec2_client = boto3.client('ec2', 'ap-southeast-1')    

def main():
    with open('InstanceData.json', 'r') as file:
        file_data = json.load(file)
        
        ec2_client.modify_volume(    
                VolumeId=file_data['VolumeId'],
                Size= int(file_data['NewSizeGib'])
        ) 

        
        while True:
            response = ec2_client.describe_volumes(
                VolumeIds=[file_data['VolumeId']])
            
            if str(response["Volumes"][0]["Size"]) == file_data['NewSizeGib']:
                return
            
            time.sleep(3)
            

if __name__ == '__main__':
    main()

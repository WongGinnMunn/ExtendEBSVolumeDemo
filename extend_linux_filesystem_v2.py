import json
import boto3
import time

ssm_client = boto3.client('ssm', 'us-east-1')

'''

Purpose: 
    Extend the file system of the volume. 

'''

def main():
    with open('InstanceData.json', 'r') as file:
        file_data = json.load(file)
        
        mount_point = "/" 
        
        '''
        mount_point is assumed to be "/". However, if the file system is not XFS or the mount point is incorrect, use the command "df-hT" through EC2 Instance Connect to determine the mount point
        
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html
        
        '''
              
                
        # ssm_client is used to run commands on one or more managed instances
        
        response = ssm_client.send_command(
            InstanceIds=[file_data["InstanceId"]], # indicates the instance to run the command on
            DocumentName="AWS-RunShellScript", # run command document name
            TimeoutSeconds=500, 
            Parameters={
                "commands": [
                    "#!/bin/bash",
                    "set -x",
                    "findmnt -T {} || exit 1".format(
                        mount_point
                    ),  # findmnt -T is to get the filesystem in specific Target or mount point. 
                    "partition=`findmnt -T {} | awk '{{print $2}}' | sed -n '2 p'`".format(
                        mount_point
                    ), 
                    
                    
                    # 1. create a string variable named "partition" 
                    # 2. findmnt -T {} to get the filesystem
                    # 3. "awk" command is used to extract the second column of the output which contains the mount point
                    # 4. sed -n '2 p' is to print only the second one of output. Hence partition is only assigned the second line output. 
                    
                    # | means execute the preceding statement and connect its stdout to the stdin of the statement which follows    
                                   
                    
                    # "deviceName=`lsblk -npo pkname $partition`", 
                    
                    
                    # -n: Do not print a header line
                    # -p: used to display the output in a stable, machine-readable format
                    # -o: Specify which output columns to print
                    # used to get the parent device (disk) of a specified partition
                    # pkname: internal parent kernel device name
                    
                    "partitionNumber=${partition#$deviceName}", # matching up the partiton and the device name and the partition number is the part where the partition string does not mtach the device name. 
                    "sudo growpart $deviceName $partitionNumber",
                    "sudo xfs_growfs -d {} || sudo resize2fs $partition".format(
                        mount_point
                    ),
                ]
            },
        )
        command_id = response["Command"]["CommandId"]
        status, status_details = get_command_status_with_wait(
            file_data["InstanceId"], command_id
        )
        
        
        if status_details == "Failed":
            raise Exception("Error extending the file system")
        
        
        return


def get_command_status_with_wait(instance_id, command_id):
    time.sleep(10)
    response = ssm_client.get_command_invocation(
        CommandId=command_id, InstanceId=instance_id
    )
    status = response["Status"]
    details = response["StatusDetails"]
    return status, details


if __name__ == '__main__':
    main()

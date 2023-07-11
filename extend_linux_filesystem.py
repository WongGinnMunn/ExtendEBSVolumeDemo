import json
import sys
import boto3
import time

ssm_client = boto3.client('ssm', 'us-east-1')

def main(arg):
    with open('InstanceData.json', 'r') as file:
        file_data = json.load(file)
        
        mount_point = "/"
        response = ssm_client.send_command(
            InstanceIds=[file_data["InstanceId"]],
            DocumentName="AWS-RunShellScript",
            TimeoutSeconds=500,
            Parameters={
                "commands": [
                    "#!/bin/bash",
                    "set -x",
                    "findmnt -T {} || exit 1".format(
                        mount_point
                    ),  # make sure that the mount point is valid
                    "partition=`findmnt -T {} | awk '{{print $2}}' | sed -n '2 p'`".format(
                        mount_point
                    ),
                    "deviceName=`lsblk -npo pkname $partition`",
                    "partitionNumber=${partition#$deviceName}",
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
        
        
        return arg


def get_command_status_with_wait(instance_id, command_id):
    time.sleep(10)
    response = ssm_client.get_command_invocation(
        CommandId=command_id, InstanceId=instance_id
    )
    status = response["Status"]
    details = response["StatusDetails"]
    return status, details


if __name__ == '__main__':
    main(sys.argv[1:])

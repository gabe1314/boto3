import boto3
from time import sleep
from sys import argv


def get_recovery_points(vault_name: str) -> list:
    pagination = True
    restore_points = []
    b = boto3.client('backup')

    res = b.list_recovery_points_by_backup_vault(
        BackupVaultName=vault_name,
        MaxResults=200
    )

    while pagination:
        for point in res['RecoveryPoints']:
            restore_points.append(point['RecoveryPointArn'])
        if 'NextToken' in res:
            res = b.list_recovery_points_by_backup_vault(
                BackupVaultName=vault_name,
                MaxResults=200,
                NextToken=res['NextToken']
            )
        else:
            pagination = False

    return restore_points

def delete_recovery_points(vault_name: str, point_arn_list: list) -> bool:
    b = boto3.client('backup')

    for index, point in enumerate(point_arn_list):
        print(f'[.] Deleting recovery point "{point}" [{index} / {len(point_arn_list)}]')
        res = b.delete_recovery_point(
            BackupVaultName=vault_name,
            RecoveryPointArn=point
        )
        sleep(1)

    return True

if __name__ == '__main__':
    vault_name = argv[1]
    recovery_points = get_recovery_points(vault_name)
    print(f'[+] Found {len(recovery_points)} recovery points! Deleting them!')
    delete_recovery_points(vault_name, recovery_points)
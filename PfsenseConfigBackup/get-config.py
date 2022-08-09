from paramiko import SSHClient
from scp import SCPClient
import pandas
import datetime
import os

BASE_DIR = './BACKUPS/'
CRED_CSV = './pfsensecreds.csv'

def Get_Config_file(username:str,server:str,localfile:str,secret:str,remotefile:str='/cf/conf/config.xml',port:int=22):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    try:
        ssh.connect(hostname=server,port=port,username=username,password=secret)
        with SCPClient(ssh.get_transport()) as scp:
            file = scp.get(remotefile,localfile)
    except Exception as error_message:
        print(error_message)
    else:
        print(f"Backup of {server} was successful")

def Create_Dir(path):
    if not os.path.isdir(path):
        print(f"{path} : Does not exist Creating")
        os.mkdir(path)


def Generate_savefilepath(firewall_id):
    weekday = datetime.datetime.now().strftime('%A')
    savefilefolder = f"{BASE_DIR}{firewall_id}/"
    savefilename = f"{firewall_id}-{weekday}-Backup.xml"
    savefilepath = savefilefolder + savefilename
    Create_Dir(BASE_DIR)
    Create_Dir(savefilefolder)
    return savefilepath

cred_data_dict = pandas.read_csv(CRED_CSV).to_dict(orient="records")
#loop trough each one
for firewall_credential in cred_data_dict:
    save_file = Generate_savefilepath(firewall_credential['site'])
    Get_Config_file(username=firewall_credential['username'],secret=firewall_credential['password'],localfile=save_file,server=firewall_credential['ipaddress'])
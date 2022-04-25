
import subprocess
import yaml

class Provision:
    def __init__(self, instance_id):
        self.instance_id = instance_id

    def create(self, password, capacity, database_type):
        command = f'''
        gcloud sql instances create {self.instance_id} \
            --database-version={database_type} \
            --root-password={password} \
            --storage-size={capacity} \
            --cpu=2 \
            --memory=4GB \
            --region=us-central1 \
            --no-backup \
            --storage-type=HDD \
            --authorized-networks=0.0.0.0/0 \
            --async
        '''

        try:
            output = subprocess.check_output(command, shell=True, text=True)
        except: 
            return f"Database with id {self.instance_id} already exists or has been deleted recently", 1

        return output, 0

    def destroy(self):
        command = f"gcloud sql instances delete {self.instance_id} -q --async"
        output = subprocess.check_output(command, shell=True, text=True)

        return output

    def get_info(self):
        command = f"gcloud sql instances describe {self.instance_id}"
        output = subprocess.check_output(command, shell=True, text=True)
        if "The Cloud SQL instance does not exist" in output:
            return "The Cloud SQL instance does not exist." 

        output_yaml = yaml.safe_load(output)
        try:
            for ip in output_yaml['ipAddresses']:
                if ip['type'] == "PRIMARY":
                    publicIP = ip['ipAddress']
        except:
            publicIP = None
        
        return {
            "creationTime": output_yaml['createTime'],
            "databaseVersion": output_yaml['databaseVersion'],
            "publicIp": publicIP,
            "name": output_yaml['name'],
            "region": output_yaml['region'],
            "dataDiskSizeGb": output_yaml['settings']['dataDiskSizeGb'],
            "dataDiskType": output_yaml['settings']['dataDiskType'],
            "state": output_yaml['state']
        }

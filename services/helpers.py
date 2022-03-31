import subprocess
from time import sleep

from settings import CA_CERT_PATH, CLIENT_CERT_FOLDER, PRIVATE_KEY_FOLDER, PKI_PATH, TA_KEY_PATH


class Container:
    def __init__(self, container_id):
        self.id = container_id

    def exec(self, script):
        docker_exec = f"docker exec -it {self.id} {script}"
        return subprocess.run(docker_exec, capture_output=True).stdout.decode("utf-8")

    def upload_file(self):
        pass

    def get_file_content(self, path):
        return self.exec(f"cat {path}")


class EasyRSA:
    def __init__(self, container):
        self.path = PKI_PATH
        self.container = container

    def create_new_client(self, client_name):
        script = f"cd {self.path} " \
                 f"| " \
                 f"easyrsa --passin=file:dh.pem --passout=file:dh.pem  build-client-full {client_name}"
        self.container.exec(script)
        sleep(5)
        return self.get_clients_data(client_name)

    def get_clients_data(self, client_name):
        ca_cert = self.container.get_file_content(CA_CERT_PATH)

        client_cert = self.container.get_file_content(f"{CLIENT_CERT_FOLDER}/{client_name}.crt")

        private_key = self.container.get_file_content(f"{PRIVATE_KEY_FOLDER}/{client_name}.key")

        ta_key = self.container.get_file_content(TA_KEY_PATH)

        return {"CA": ca_cert, "client_certificate": client_cert, "pk": private_key, "ta": ta_key}


def get_container_id(container_name):
    cmd = ['docker', 'ps', '-a']
    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    cmd = ['grep', container_name]
    grep = subprocess.Popen(cmd, stdin=ps.stdout, stdout=subprocess.PIPE,
                            encoding='utf-8')
    ps.stdout.close()
    output, _ = grep.communicate()
    python_processes = output.split('\n')
    return output.split(" ")[0]
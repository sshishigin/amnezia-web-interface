import subprocess
from pprint import pprint
from time import sleep

from settings import CA_CERT_PATH, CLIENT_CERT_FOLDER, PRIVATE_KEY_FOLDER, PKI_PATH, TA_KEY_PATH


class Container:
    def __init__(self, container_id):
        self.id = container_id

    def exec(self, script, with_output=False):
        docker_exec = f"docker exec -it {self.id} {script}"
        if with_output:
            try:
                return subprocess.check_output(docker_exec.split(" ")).decode("utf-8")
            except subprocess.CalledProcessError as e:
                pprint({field: getattr(e, field) for field in dir(e) if not field.startswith("__")})

        subprocess.call(docker_exec)

    def upload_file(self):
        pass

    def get_file_content(self, path):
        return self.exec(f"cat {path}", with_output=True)


class EasyRSA:
    def __init__(self, container):
        self.path = PKI_PATH
        self.container = container

    def create_new_client(self, client_name):
        cmd = f"cd /opt/amnezia/openvpn | easyrsa --passin=file:dh.pem --passout=file:dh.pem build-client-full {client_name} nopass"
        self.container.exec(cmd, with_output=True)
        sleep(10)
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
    return output.split(" ")[0]

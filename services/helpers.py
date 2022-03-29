import subprocess

from settings import CA_CERT_PATH, CLIENT_CERT_FOLDER, PRIVATE_KEY_FOLDER, PKI_PATH


class Container:
    def __init__(self, container_id):
        self.id = container_id

    def exec(self, script, with_output=False):
        docker_exec = f"docker exec -it {self.id} {script}"
        if with_output:
            return subprocess.check_output(docker_exec.split(" ")).decode("utf-8")
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
        script = f"cd {self.path} " \
                 f"| " \
                 f"easyrsa --passin=file:dh.pem --passout=file:dh.pem  build-client-full {client_name}"
        self.container.exec(script)


    def get_clients_data(self, client_name):
        ca_cert = self.container.get_file_content(CA_CERT_PATH)

        client_cert = self.container.get_file_content(f"{CLIENT_CERT_FOLDER}/{client_name}.crt")

        private_key = self.container.get_file_content(f"{PRIVATE_KEY_FOLDER}/{client_name}.key")

        return {"CA": ca_cert, "client_certificate": client_cert, "pk": private_key}

import subprocess

PKI_PATH = "/opt/amnezia/openvpn"
OPENVPN_CONTAINER_ID = subprocess.check_output("docker ps | grep openvpn".split(" "))[0]
CA_CERT_PATH = "/opt/amnezia/openvpn/ca.crt"
CLIENT_CERT_FOLDER = "/opt/amnezia/openvpn/pki/issued"
PRIVATE_KEY_FOLDER = "/opt/amnezia/openvpn/pki/private"
TA_KEY_PATH = "/opt/amnezia/openvpn/ta.key"
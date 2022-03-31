from services.helpers import get_container_id

PKI_PATH = "/opt/amnezia/openvpn"
OPENVPN_CONTAINER_ID = get_container_id("openvpn")
CA_CERT_PATH = "/opt/amnezia/openvpn/ca.crt"
CLIENT_CERT_FOLDER = "/opt/amnezia/openvpn/pki/issued"
PRIVATE_KEY_FOLDER = "/opt/amnezia/openvpn/pki/private"
TA_KEY_PATH = "/opt/amnezia/openvpn/ta.key"
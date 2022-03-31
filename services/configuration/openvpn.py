from copy import copy

from services.configuration.general import Configurator
from services.helpers import EasyRSA, Container, get_container_id

template = \
"""
client
dev tun
proto $OPENVPN_TRANSPORT_PROTO
resolv-retry infinite
nobind
persist-key
persist-tun
$OPENVPN_NCP_DISABLE
cipher $OPENVPN_CIPHER
auth $OPENVPN_HASH
verb 3
tls-client
tls-version-min 1.2
key-direction 1
remote-cert-tls server
redirect-gateway def1 bypass-dhcp

dhcp-option DNS $PRIMARY_DNS
dhcp-option DNS $SECONDARY_DNS
block-outside-dns

remote $REMOTE_HOST $OPENVPN_PORT

<ca>
$OPENVPN_CA_CERT
</ca>
<cert>
$OPENVPN_CLIENT_CERT
</cert>
<key>
$OPENVPN_PRIV_KEY
</key>
<tls-auth>
$OPENVPN_TA_KEY
</tls-auth>
"""


class OpenVPNClientConfigurator(Configurator):
    def __init__(self):
        OPENVPN_CONTAINER_ID = get_container_id("openvpn")
        self.container = Container(OPENVPN_CONTAINER_ID)

    def generate_configuration(self, client_name, platform="linux"):
        rsa = EasyRSA(self.container)
        data = rsa.create_new_client(client_name)
        data.update({"platform": platform})
        config = self.__build_config(data)
        return config

    def __build_config(self, data):
        config = template
        OpenVPNServerConfigurator().get_server_settings()

        config = config.replace("$OPENVPN_CA_CERT", data.get("CA"))
        config = config.replace("$OPENVPN_CLIENT_CERT", data.get("client_certificate"))
        config = config.replace("$OPENVPN_PRIV_KEY", data.get("pk"))
        config = config.replace("$OPENVPN_TA_KEY", data.get("ta"))
        if data.get("platform") != "windows":
            config = config.replace("block-outside-dns", "")
        print(config)
        return config


class OpenVPNServerConfigurator(Configurator):
    def __init__(self):
        OPENVPN_CONTAINER_ID = get_container_id("openvpn")
        self.container = Container(OPENVPN_CONTAINER_ID)

    def get_server_settings(self):
        server_config = self.container.get_file_content("/opt/amnezia/openvpn/server.conf")
        print(server_config, type(server_config))



from OpenSSL import crypto

from services.configuration.general import Configurator
from services.helpers import EasyRSA, Container
from settings import PKI_PATH, OPENVPN_CONTAINER_ID

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


class OpenVPNConfigurator(Configurator):
    def __init__(self):
        self.container = Container(OPENVPN_CONTAINER_ID)

    def generate_config(self, client_name):
        rsa = EasyRSA(PKI_PATH, container=self.container)
        rsa.create_new_client(client_name)





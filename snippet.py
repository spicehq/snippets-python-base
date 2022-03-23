import os
from pathlib import Path
import ssl
import urllib.request

from pyarrow import flight


# Check for gRPC required Google certificate file
if not Path('/usr', 'share', 'grpc', 'roots.pem').exists():
    env_name = 'GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'
    if env_name not in os.environ or not Path(os.environ[env_name]).exists():
        tls_root_certs = './roots.pem'
        if not Path(tls_root_certs).exists():
            print('Downloading gRPS root certificates')
            # Do not verify certs for https (Mac issue)
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve('https://pki.google.com/roots.pem', tls_root_certs)
        os.environ[env_name] = tls_root_certs

client = flight.connect('grpc+tls://flight.spiceai.io')
headers = [client.authenticate_basic_token('', 'API_KEY')]
options = flight.FlightCallOptions(headers=headers)

query = 'SELECT * FROM eth.blocks ORDER BY number DESC LIMIT 10;'
flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)
reader = client.do_get(flight_info.endpoints[0].ticket, options)

print(reader.read_pandas())

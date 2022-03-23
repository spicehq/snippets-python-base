import os
from pathlib import Path
import urllib.request

from pyarrow import flight


# Check for gRPC required Google certificate file
tls_root_certs = None
if not Path('/usr', 'share', 'grpc', 'roots.pem').exists():
    env_name = 'GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'
    if env_name in os.environ and not Path(os.environ[env_name]).exists():
        print('Downloading gRPS root certificates')
        tls_root_certs = './roots.pem'
        urllib.request.urlretrieve('https://pki.google.com/roots.pem', tls_root_certs)

client = flight.connect('grpc+tls://flight.spiceai.io', tls_root_certs=tls_root_certs)
headers = [client.authenticate_basic_token('', 'API_KEY')]
options = flight.FlightCallOptions(headers=headers)

query = 'SELECT * FROM eth.blocks ORDER BY number DESC LIMIT 10;'
flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)
reader = client.do_get(flight_info.endpoints[0].ticket, options)

print(reader.read_pandas())

import os
from pathlib import Path
import ssl
import tempfile
import urllib.request

from pyarrow import flight


# Check for gRPC certificates
if not (Path(Path.cwd().absolute().anchor) / 'usr' / 'share' / 'grpc' / 'roots.pem').exists():
    env_name = "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"
    if env_name not in os.environ or not Path(os.environ[env_name]).exists():
        tls_root_certs = Path(tempfile.gettempdir()) / "isrgrootx1.pem"
        if not Path(tls_root_certs).exists():
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve("https://letsencrypt.org/certs/isrgrootx1.pem", str(tls_root_certs))
        os.environ[env_name] = str(tls_root_certs)

client = flight.connect('grpc+tls://flight.spiceai.io')
headers = [client.authenticate_basic_token('', 'API_KEY')]
options = flight.FlightCallOptions(headers=headers)

query = 'SELECT * FROM eth.blocks ORDER BY number DESC LIMIT 10;'
flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)
reader = client.do_get(flight_info.endpoints[0].ticket, options)

print(reader.read_pandas())

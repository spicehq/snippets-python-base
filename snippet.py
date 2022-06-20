# Install with: pip install git+https://github.com/spiceai/spice-py
from spicepy import Client

client = Client('API_KEY')
reader = client.query('SELECT * FROM eth.recent_blocks ORDER BY number DESC;')
print(reader.read_pandas())

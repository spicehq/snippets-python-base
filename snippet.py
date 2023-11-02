# Install with: pip install git+https://github.com/spiceai/spicepy@v1.0.0
from spicepy import Client

client = Client('API_KEY')
reader = client.query('SELECT * FROM eth.recent_blocks ORDER BY number DESC;')
print(reader.read_pandas())

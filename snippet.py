from spicepy import Client

client = Client('API_KEY')
reader = client.query('SELECT * FROM eth.blocks ORDER BY number DESC LIMIT 10;')
print(reader.read_pandas())

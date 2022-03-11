from pyarrow import flight

client = flight.connect('grpc+tls://flight.spiceai.io')

headers = [client.authenticate_basic_token('', 'API_KEY')]
options = flight.FlightCallOptions(headers=headers)

query = 'SELECT * FROM eth.blocks ORDER BY number DESC LIMIT 10;'
flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)
reader = client.do_get(flight_info.endpoints[0].ticket, options)

print(reader.read_pandas())

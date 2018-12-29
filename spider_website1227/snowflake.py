import snowflake.client

host = '192.168.10.145'
port = 30001
snowflake.client.setup(host, port)

snowflake.client.get_guid()
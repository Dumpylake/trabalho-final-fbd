import psycopg2 # type: ignore

def get_connection():
    return psycopg2.connect(
        dbname="petshop",
        user="postgres",
        password="postgres",
        host="localhost",
        client_encoding='utf8'
    )
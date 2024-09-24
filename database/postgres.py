import psycopg2

from config.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_DB,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    sslmode='disable'
)

cur=conn.cursor()
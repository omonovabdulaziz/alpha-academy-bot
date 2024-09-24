import psycopg2

from config.config import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


def get_db_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )


def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT UNIQUE NOT NULL,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100)
        );
        CREATE TABLE IF NOT EXISTS results(
        code varchar PRIMARY KEY ,
        math_ball int NOT NULL DEFAULT 0,
        english_ball int NOT NULL DEFAULT 0,
        common_ball int NOT NULL Default 0,
        user_name varchar NOT NULL ,
        user_surname varchar NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

import psycopg2

# Parâmetros de conexão
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5432
DEFAULT_USERNAME = "postgres"
DEFAULT_PASSWORD = "postgres"
DEFAULT_DBNAME = "series"

# Estabelecer conexão com o PostgreSQL
def establish_connection():
    try:
        conn = psycopg2.connect(
            host=DEFAULT_HOST,
            port=DEFAULT_PORT,
            user=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
            database=DEFAULT_DBNAME
        )
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        print()


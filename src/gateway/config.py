import os


def get_postgres_uri():
    host = os.environ.get('DB_HOST', '192.168.1.206')
    port = 5432 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'ib_dev')
    user, db_name = 'ib_dev', 'ib_dev'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5000 if host == 'localhost' else 80
    return f"http://{host}:{port}"


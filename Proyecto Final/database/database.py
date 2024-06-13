import psycopg2
import json

def connect_to_db():
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)

        db_config = config["database"]
        
        connection = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            dbname=db_config["name"],
            user=db_config["user"],
            password=db_config["password"]
        )

        cursor = connection.cursor()

        return connection, cursor

    except Exception as e:
        print('Database error:', e)
        return None, None

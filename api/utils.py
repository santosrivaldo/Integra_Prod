def create_table_if_not_exists(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id SERIAL PRIMARY KEY,
            username TEXT,
            appname TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            active BOOLEAN,
            bucket TEXT,
            timestamp TIMESTAMP
        )
    ''')
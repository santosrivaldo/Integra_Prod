CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    username TEXT,
    appname TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    active BOOLEAN,
    timestamp TIMESTAMP
);

class Queries:
    create_password_table = """CREATE TABLE IF NOT EXISTS passwords (
id INTEGER PRIMARY KEY AUTOINCREMENT,
label TEXT NOT NULL,
password_hash TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""

    does_table_exist = """SELECT name FROM sqlite_master WHERE type='table' AND name=?;"""

    read_all_data_from_passwords = """select * from passwords;"""

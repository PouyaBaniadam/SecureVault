class Queries:
    create_password_table = """CREATE TABLE IF NOT EXISTS passwords (
                            id INTEGER PRIMARY KEY,
                            label TEXT NOT NULL UNIQUE,
                            encrypted_password BLOB NOT NULL,
                            nonce BLOB NOT NULL,
                            tag BLOB NOT NULL
                          )
"""

    add_password = """INSERT INTO passwords (label, encrypted_password, nonce, tag) 
                              VALUES (?, ?, ?, ?)
"""

    retrieve_password = """SELECT encrypted_password, nonce, tag FROM passwords WHERE label = ?"""

    update_password = """UPDATE passwords SET encrypted_password = ?, nonce = ?, tag = ? WHERE label = ?"""

    delete_password = """DELETE FROM passwords WHERE label = ?"""

    list_passwords = """SELECT label FROM passwords"""

    load_labels = """SELECT label FROM passwords"""
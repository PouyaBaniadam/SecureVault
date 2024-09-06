class Queries:
    create_password_table = """
    CREATE TABLE IF NOT EXISTS passwords (
        label TEXT PRIMARY KEY,
        encrypted_password BLOB,
        nonce BLOB,
        tag BLOB,
        salt BLOB
    );
"""


    add_password = """
    INSERT INTO passwords (label, encrypted_password, nonce, tag, salt)
    VALUES (?, ?, ?, ?, ?);
"""

    retrieve_password = """
    SELECT encrypted_password, nonce, tag, salt FROM passwords WHERE label = ?;
"""

    update_password = """UPDATE passwords SET encrypted_password = ?, nonce = ?, tag = ?, salt = ? WHERE label = ?;"""

    delete_password = """DELETE FROM passwords WHERE label = ?"""

    list_passwords = """SELECT label FROM passwords"""

    load_labels = """SELECT label FROM passwords"""

    load_all_passwords = """
    SELECT label, encrypted_password, nonce, tag, salt
    FROM passwords;
"""

    delete_password_table = """DELETE FROM passwords"""

    insert_or_ignore_passwords = """
    INSERT OR IGNORE INTO passwords (label, encrypted_password, nonce, tag, salt) VALUES (?, ?, ?, ?, ?)
"""
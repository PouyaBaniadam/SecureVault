import secrets
import sqlite3

from database.queries import Queries
from statics.settings import SETTINGS

NUM_RECORDS = 100
DB_NAME = f"../{SETTINGS.DB_NAME}"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

create_password_table = Queries.create_password_table
cursor.execute(create_password_table)
conn.commit()


def generate_random_bytes(length):
    return secrets.token_bytes(length)


# Function to generate a random label
def generate_random_label():
    return secrets.token_hex(8)  # Generate a random hex string of length 16 (8 bytes)


for _ in range(NUM_RECORDS):
    label = generate_random_label()
    encrypted_password = generate_random_bytes(32)
    nonce = generate_random_bytes(12)
    tag = generate_random_bytes(16)
    salt = generate_random_bytes(16)

    cursor.execute(
        Queries.insert_or_ignore_passwords, (label, encrypted_password, nonce, tag, salt)
    )

conn.commit()
conn.close()

print(f"Inserted {NUM_RECORDS} random records into the database.")

import os
import sqlite3

DATABASE = 'db_teleguard.db'  # novo banco sem senha

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DATABASE)
    return sqlite3.connect(db_path)

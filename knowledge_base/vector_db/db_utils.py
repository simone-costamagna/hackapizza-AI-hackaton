import logging
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME
        )
        return connection
    except Exception as e:
        logging.error(f"Failed to connect: {e}")
        return None


def add_document(filename, chunks):
    """Add a row to the Document table. If the file already exists, delete it and return a new ID."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Documents (filename, chunks) VALUES (%s, %s) RETURNING filename;", (filename, chunks,))
        connection.commit()
        document_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return document_id


def read_document(filename):
    """Read a row from the Document table by its ID."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Documents WHERE filename = %s;", (filename,))
        row = cursor.fetchone()
        if row:
            keys = [desc[0] for desc in cursor.description]
            result = dict(zip(keys, row))
        else:
            result = None
        cursor.close()
        connection.close()
        return result


def update_document(filename, chunks):
    """Update a row in the Document table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE Documents SET chunks = %s WHERE filename = %s;", (chunks, filename))
        connection.commit()
        cursor.close()
        connection.close()


def remove_document(filename):
    """Remove a row from the Document table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Documents WHERE filename = %s;", (filename,))
        connection.commit()
        cursor.close()
        connection.close()


def add_chunk(file_id):
    """Add a row to the Chunks table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Chunks (file) VALUES (%s) RETURNING id;", (file_id,))
        connection.commit()
        new_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return new_id


def read_chunk(row_id):
    """Read a row from the Chunks table by its ID."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Chunks WHERE id = %s;", (row_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row


def remove_chunk(row_id):
    """Remove a row from the Chunks table."""
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Chunks WHERE id = %s;", (row_id,))
        connection.commit()
        cursor.close()
        connection.close()

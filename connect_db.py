import sqlite3

def connectDb() -> sqlite3.Connection:
    """Estabilishes a connection with the local "book_pdf" database.

    Returns:
        sqlite3.Connection: An active connection with the "book_pdf" database.
    """

    conn = sqlite3.connect("book_pdf.db") #Local database of book pdfs

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, name TEXT, category TEXT, num_pages INT, file_size FLOAT, file_path TEXT)")
    cursor.close()

    return conn

def disconnectDB(conn:sqlite3.Connection) -> None:
    """Closes the connection with the local "book_pdf" database

    Args:
        conn (sqlite3.Connection): An active connection with the "book_pdf" database.
    """
    
    if conn:
        conn.close()
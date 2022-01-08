from sqlite3 import Cursor

def create_db(conn) -> Cursor:
    cursor = conn.cursor()

    # for testing purposes we are droping all tables every time
    cursor.execute("DROP TABLE IF EXISTS items;")

    print("creating database")
    cursor.execute(
        r"""
        CREATE TABLE IF NOT EXISTS items (
            name TEXT NOT NULL PRIMARY KEY,
            description TEXT,
            notes TEXT,
            info JSON DEFAULT('{}')
        );
    """
    )

    return cursor


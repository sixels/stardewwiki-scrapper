def create_db(conn):
    db = conn.cursor()

    # for testing purposes we are droping all tables every time
    db.execute("DROP TABLE IF EXISTS weapons;")
    db.execute("DROP TABLE IF EXISTS items;")

    print("creating database")
    db.execute("""
        CREATE TABLE IF NOT EXISTS weapons (
            name TEXT NOT NULL PRIMARY KEY,
            type TEXT,
            level TEXT,
            description TEXT,
            damage TEXT,
            critical_chance TEXT,
            stats TEXT,
            location TEXT,
            purchase_price TEXT,
            sell_price TEXT
        );
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            name TEXT NOT NULL PRIMARY KEY,
            description TEXT,
            notes TEXT,
            aditional TEXT
        );
    """)
mport sqlite3

def setup_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    print("Cleaning up old data...")
    cursor.execute("DROP TABLE IF EXISTS Loans")
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("DROP TABLE IF EXISTS Members")
    
    print("Creating new tables...")
    cursor.execute("""CREATE TABLE Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        rating REAL DEFAULT 0.0
        )
        """)
    cursor.execute("""
        CREATE TABLE Members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE Loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_ptr INTEGER,
            member_ptr INTEGER,
            loan_date DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_ptr) REFERENCES Books (book_id),
            FOREIGN KEY (member_ptr) REFERENCES Members (member_id)
        )
    """)

    print("Seeding data...")
    books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 4.2),
        ('1984', 'George Orwell', 4.8),
        ('The Hobbit', 'J.R.R. Tolkien', 4.9),
        ('Python for Beginners', 'AI Guru', 3.5)
    ]
    cursor.executemany("INSERT INTO Books (title, author, rating) VALUES (?, ?, ?)", books)

    members = [('Alice Smith'), ('Bob Jones'), ('Charlie Brown')]
    cursor.executemany("INSERT INTO Members (member_name) VALUES (?)", [(m,) for m in members])

    loans = [(3, 1), (3, 2), (2, 1)]
    cursor.executemany("INSERT INTO Loans (book_ptr, member_ptr) VALUES (?, ?)", loans)
    conn.commit()
    conn.close()
    print("Database 'library.db' is refreshed and ready!")

if __name__ == "__main__":
    setup_database()
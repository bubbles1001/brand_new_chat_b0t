import sqlite3

def create_database():
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    
    # Create Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            hire_date TEXT NOT NULL
        )
    ''')
    
    # Create Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            manager TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    employees_data = [
        ("Alice", "Sales", 50000, "2021-01-15"),
        ("Bob", "Engineering", 70000, "2020-06-10"),
        ("Charlie", "Marketing", 60000, "2022-03-20")
    ]
    
    departments_data = [
        ("Sales", "Alice"),
        ("Engineering", "Bob"),
        ("Marketing", "Charlie")
    ]
    
    cursor.executemany("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)", employees_data)
    cursor.executemany("INSERT INTO departments (name, manager) VALUES (?, ?)", departments_data)
    
    # Commit and close connection
    conn.commit()
    conn.close()
    print("Database setup complete! ✅")

# Run the function
if __name__ == "__main__":
    create_database()

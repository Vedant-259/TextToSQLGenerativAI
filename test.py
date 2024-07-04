import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("student.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Check the table data
print("Data in STUDENT table:")
try:
    data = cursor.execute("SELECT * FROM STUDENT;")
    for row in data:
        print(row)
except sqlite3.OperationalError as e:
    print(f"SQL error: {e}")

# Commit the changes and close the connection
connection.commit()
connection.close()

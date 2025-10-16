import csv
import sqlite3

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect('insurance.db')
cursor = conn.cursor()

# Create a table (adjust column names and types as needed)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS insurance (
        id INTEGER PRIMARY KEY,
        age INTEGER,
        sex TEXT,
        bmi REAL,
        children INTEGER,
        smoker TEXT,
        region TEXT,
        charges REAL
    )
''')

# Open and read the CSV file
with open('Medical Insurance Cost Dataset.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row if present

    # Insert data into the table
    for row in reader:
        cursor.execute("INSERT INTO insurance (age, sex, bmi, children, smoker, region, charges) VALUES (?, ?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

# Commit changes and close connection
conn.commit()
conn.close()
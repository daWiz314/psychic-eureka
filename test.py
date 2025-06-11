import sqlite3
import json

conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
cur = conn.cursor()

# Delete existing table
cur.execute('DROP TABLE IF EXISTS documents')

# Create a table to store data
cur.execute('''CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    data TEXT,
                    test TEXT
                )''')

# sample_data 

json_data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "skills": ["Python", "Django", "Flask"]
}

json_data2 = {
    "name": "Mary Doe",
    "age": 33,
    "city": "New York",
    "skills": ["Python", "Django", "Flask"]
}
# Insert JSON data into the table
cur.execute('INSERT INTO documents (data) VALUES (?)', (json.dumps(json_data),))
cur.execute('INSERT INTO documents (data) VALUES (?)', (json.dumps(json_data2),))
cur.execute('UPDATE documents SET test = ? WHERE id = ?', (json.dumps(json_data), 2))
# Commit the changes
conn.commit()

# Fetch and print the data
cur.execute('SELECT * FROM documents')
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Data: {json.loads(row[1])}, Test: {row[2]}")


# Fetch only the second ID
cur.execute('SELECT * FROM documents WHERE id = ?', (2,))
row = cur.fetchone()
if row:
    print(f"ID: {row[0]}, Data: {json.loads(row[1])}, Test: {row[2]}")

# Fetch only the test data from the second ID
cur.execute('SELECT test FROM documents WHERE id = ?', (2,))
test_row = cur.fetchone()
if test_row:
    print(f"Test Data: {json.loads(test_row[0])}")

print("\n\n")
data = json.loads(test_row[0])
print(f"Name: {data['name']}, Age: {data['age']}, City: {data['city']}, Skills: {', '.join(data['skills'])}")
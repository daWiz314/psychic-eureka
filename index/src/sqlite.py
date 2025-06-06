import datetime
import os
import sqlite3

def connect() -> sqlite3.Connection:
	cd = __file__.rsplit('/', 2)[0] + "/"
	# Check if database file exists
	if (not os.path.exists(cd+"db/users.sqlite")):
		# then make the file
		if not os.path.exists(cd+"db"):
			os.makedirs(cd+"db")

		# Create the database file
		with open(cd+"db/users.sqlite", 'w') as f:
			pass

	# Set up the database
	print(cd)
	db = sqlite3.connect(cd+"/db/users.sqlite", check_same_thread=False)
	return db

def sql_set_up() -> None:
	db = connect()
	# Delete the table after every set up of server
	db.execute('''
				DROP TABLE IF EXISTS users
				''')
	# Create new table with 3 columns
	# Name, message, password
	db.execute('''
			   CREATE TABLE IF NOT EXISTS users (
					name TEXT UNIQUE, 
					display_name TEXT UNIQUE,
					title TEXT,
					message TEXT,
					times TEXT,
					password TEXT,
					id INTEGER PRIMARY KEY AUTOINCREMENT
			   )
			   ''')
	db.commit()
	db.close()
	print("Database set up complete.")

def add_user(display_name, title, message, password) -> bool:
	"""
	Adds a user to the database, if they don't already exist.
	"""
	db = connect()
	cursor = db.cursor()

	name = display_name.lower()
	
	cursor.execute('''
					 SELECT name FROM users WHERE name = ?
					 ''', (name,))
	result = cursor.fetchone()
	if result:
		print(f"User {name} already exists in the database.")
		db.close()
		return False

	cursor.execute('''
				   INSERT INTO users (name, display_name, title, message, password) 
				   VALUES (?, ?, ?, ?, ?)
				   ''', (name, display_name, title, message, password))
	
	db.commit()
	db.close()
	print(f"User {name} added to the database.")
	return True

def get_hashed_password(user) -> str | None:
	"""
	Retrieves the hashed password for a user from the database.
	"""
	db = connect()
	cursor = db.cursor()
	
	cursor.execute('''
				   SELECT password FROM users WHERE name = ?
				   ''', (user.lower(),))
	
	result = cursor.fetchone()
	db.close()
	
	if result:
		return result[0]
	else:
		return None

def get_feed() -> list[dict]:
	"""
	Retrieves all messages from the database.
	"""
	db = connect()
	cursor = db.cursor()
	
	cursor.execute('''
				   SELECT display_name, title, message, times FROM users
				   ''')
	
	data = cursor.fetchall()
	db.close()
	
	feed = []
	for row in data:
		print(row)
		if row[1] is None:
			# Skip rows where the title is None
			continue
		if row[2][0] is None:
			# Skip rows where the message is None
			continue
		
		if ";;;" in row[2]:
			# Split the message if it contains ";;;"
			messages = row[2].split(";;;")
			titles = row[1].split(";;;")
			times = row[3].split(";;;")

			for i, msg in enumerate(messages):
				feed.append({
					'name': row[0],
					'title': titles[i],
					'message': msg,
					'time': times[i]
				})
			continue
		else:
			feed.append({
				'name': row[0],
				'title': row[1],
				'message': row[2],
				'time': row[3]
			})
	print(feed)
	return feed

def sql_create_message(user, title, message) -> None:
	"""
	Creates a message in the database.
	"""

	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	

	db = connect()
	cursor = db.cursor()
	
	cursor.execute('''
					SELECT message FROM users WHERE name = ?
				   ''', (user,))
	result = cursor.fetchone()
	if result and result[0] is not None:
		messages = result[0] + ";;;" + message
		message = messages

	cursor.execute('''
				   SELECT title FROM users WHERE name = ?
				   ''', (user,))
	result = cursor.fetchone()
	if result and result[0] is not None:
		titles = result[0] + ";;;" + title
		title = titles
	
	cursor.execute('''
				   SELECT times FROM users WHERE name = ?
				   ''', (user,))
	result = cursor.fetchone()
	if result and result[0] is not None:
		times = result[0] + ";;;" + date
		date = times

	cursor.execute('''
				   UPDATE users SET title = ? WHERE name = ?
				   ''', (title, user))

	cursor.execute('''
				   UPDATE users SET message = ? WHERE name = ?
				   ''', (message, user))
	
	cursor.execute('''
					 UPDATE users SET times = ? WHERE name = ?
					 ''', (date, user))
	
	db.commit()
	db.close()
	print("Message created in the database.")

if __name__ == "__main__":
	sql_set_up()
	print("SQLite database setup complete.")
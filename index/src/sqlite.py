import datetime
import json
import os
import sqlite3

class SQLiteHandler:
	"""
	A class to handle SQLite database operations.
	"""

	def __init__(self):
		# Get the path to the database file
		self.db_path = __file__.rsplit('/', 2)[0] + "/db/users.sqlite"
		if not os.path.exists(self.db_path):
			# Create the database file if it does not exist
			if not os.path.exists(os.path.dirname(self.db_path)):
				os.makedirs(os.path.dirname(self.db_path))
			with open(self.db_path, 'w') as f:
				pass



		####
		"""
		
		DOING THIS ONLY WORKS BECAUSE THE DATABASE IS SO SMALL
		If we were to have a larger database, we should have everything allocated in the users table with their data
		I am just doing this for easier organization and to keep the code simple for now.
		We will have 3 tables:
			1. users: To store user information
			2. posts: To store posts made by users
			3. notes: To store notes made by users

		"""
		###
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cur = db.cursor()
		# Create the users table
		cur.execute('''
				CREATE TABLE IF NOT EXISTS users (
					name TEXT UNIQUE,
					display_name TEXT UNIQUE,
					password TEXT NOT NULL,
					posts TEXT,
			 		notes TEXT,
					id INTEGER PRIMARY KEY AUTOINCREMENT
				)''')
		# Create the posts table
		cur.execute('''
			  	CREATE TABLE IF NOT EXISTS posts (
			  		owner TEXT,
			  		post TEXT,
			  		id INTEGER PRIMARY KEY AUTOINCREMENT
			  	) ''')
		# Create the notes table
		cur.execute('''
			  	CREATE TABLE IF NOT EXISTS notes (
			  		owner TEXT,
			  		note TEXT,
			  		shared_with TEXT,
			  		id INTEGER PRIMARY KEY AUTOINCREMENT
			  	) ''')
		
		db.commit()
		db.close()

	def connect(self):
		"""
		Connects to the SQLite database.
		"""
		try:
			if not os.path.exists(self.db_path):
				raise FileNotFoundError(f"Database file {self.db_path} does not exist.")
		except FileNotFoundError as e:
			print("Error:", e)
			return False
		
		self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
		return True
	
	def add_user(self, name, password):
		"""
		Adds a user to the database.
		Args:
			name (str): The name of the user.
			password (str): The HASHED password of the user.
		"""

		# First check if they exist
		if self.user_exists(name):
			print(f"User {name} already exists in the database.")
			return False
		
		# If not, then add them
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		cursor.execute('''
				 INSERT INTO users (name, display_name, password)
				 VALUES (?, ?, ?)
				 ''', (name.lower(), name, password))
		db.commit()
		db.close()
	
	def user_exists(self, name):
		"""
		Checks if a user exists in the database.
		Args:
			name (str): The name of the user.
		Returns:
			bool: True if the user exists, False otherwise.
		"""
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		
		cursor.execute('''
						SELECT name FROM users WHERE name = ?
						''', (name.lower(),))
		
		result = cursor.fetchone()
		db.close()
		
		return result is not None

	def get_hashed_password(self, name):
		"""
		Retrieves the hashed password of a user from the database.
		Args:
			name (str): The name of the user.
		Returns:
			str: The hashed password of the user, or None if the user does not exist.
		"""

		# First check if they exist
		if not self.user_exists(name):
			print(f"User {name} does not exist in the database.")
			return None
		# Then get the password
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		cursor.execute('''
					 SELECT password FROM users WHERE name = ?
					 ''', (name.lower(),))
		result = cursor.fetchone()
		db.close()
		if result:
			return result[0]
		else:
			print(f"User {name} does not exist in the database.")
			return None

	def get_feed(self):
		"""
		Retrieves all messages from the database.
		Returns:
			list[dict]: A list of dictionaries containing the feed data.
		"""
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		
		cursor.execute('''
					 SELECT owner, post, id FROM posts
					 ORDER BY id DESC
					 ''')
		
		data = cursor.fetchall()
		db.close()

		# print(data)
		# It will load the data as such
		# ('display_name', '[{"title": "Title 1", "message": "Message 1", "time": "2023-10-01 12:00:00"}]')
		# So we will need to have another dictionary to hold the display name and then the posts

		filter_feed = []
		feed = []
		for row in data:
			display_name = row[0]
			posts = row[1]
			if posts is None:
				continue
			container = json.loads(posts)
			print(container)
			feed.append({
				'name': display_name,
				'title': container[0]['title'],
				'post': container[0]['message'],
				'time': container[0]['time']
				})
		
		"""
			Data example:
			[
				{ 'name': 'John Doe',
			  		'posts': [
						{'title': 'Title 1', 'message': 'Message 1', 'time': '2023-10-01 12:00:00'},
			            {'title': 'Title 2', 'message': 'Message 2', 'time': '2023-10-02 12:00:00'}
					]
				},
			 { 'name': 'Jane Doe',
			  		'posts': [
						{'title': 'Title 3', 'message': 'Message 3', 'time': '2023-10-03 12:00:00'}
					]
				}
			]
		"""
		return feed
	
	def create_message(self, user, title, message):
		"""
		Creates a message in the database.
		Args:
			user (str): The name of the user.
			message (str): The message to be created.
		"""

		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		# First check if they exist
		if not self.user_exists(user):
			print(f"User {user} does not exist in the database.")
			return
		
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		
		message = json.dumps([{
			'title': title,
			'message': message,
			'time': date
		}])

		cursor.execute('''
				 	INSERT INTO posts (owner, post)
					VALUES (?, ?)
				 ''', (user.lower(), message))
		
		db.commit()
		db.close()
	
	def create_note(self, user, note, shared_with=None):
		"""
		Creates a note in the database.
		Args:
			user (str): The name of the user.
			note (str): The note to be created.
			shared_with (list[str], optional): A list of users with whom the note is shared. Defaults to None.
		"""
		
		# First check if they exist
		if not self.user_exists(user):
			print(f"User {user} does not exist in the database.")
			return
		
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		
		
		notes = json.dumps([{
			'note': note,
			'time': date,
		}])

		# Push it to the table
		cursor.execute('''
					INSERT INTO notes (owner, note, shared_with)
					VALUES (?, ?, ?)
					''', (user.lower(), notes, shared_with if shared_with else "[]"))
		
		# Commit the changes and close the connection

		db.commit()
		db.close()

	def get_notes(self, user):
		"""
		Retrieves notes for a user from the database.
		Args:
			user (str): The name of the user.
		Returns:
			(list[str, None], list[str, None]): Returns a tuple containing two lists:
				1. Notes owned by the user.
				2. Notes shared with the user.
		"""
		
		# First check if they exist
		if not self.user_exists(user):
			print(f"User {user} does not exist in the database.")
			return []
		
		db = sqlite3.connect(self.db_path, check_same_thread=False)
		cursor = db.cursor()
		
		cursor.execute('''
				 SELECT owner, note, shared_with, id FROM notes
				 order by id desc
				 ''')
		
		result = cursor.fetchall()
		db.close()
		data = []
		for row in result:
			if row[1] is None:
				continue
			data.append({
				'owner': row[0],
				'note': json.loads(row[1]),
				'shared_with': json.loads(row[2]),
				'id': row[3]
			})

		return_data = []
		for row in data:
			if row['owner'] == user.lower() or user.lower() in row['shared_with']:
				return_data.append({
					'owner': row['owner'],
					'note': row['note'][0]["note"],
					'time': row['note'][0]["time"],
					'shared_with': row['shared_with'],
					'id': row['id']
				})
			else:
				continue
		
		notes = []
		shared_with = []

		for item in return_data:
			if item['owner'] == user.lower():
				notes.append(item)
			else:
				shared_with.append(item)
		print("Notes:", notes)
		print("Shared with:", shared_with)
		return (notes, shared_with)
		

def lcl_connect() -> sqlite3.Connection:
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
	# print(cd)
	db = sqlite3.connect(cd+"/db/users.sqlite", check_same_thread=False)
	return db

def sql_set_up() -> None:
	db = lcl_connect()
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
					notes TEXT,
					notes_shared_with TEXT,
					id INTEGER PRIMARY KEY AUTOINCREMENT
			   )
			   ''')
	db.commit()
	db.close()
	print("Database set up complete.")

def add_user(display_name, password) -> bool:
	"""
	Adds a user to the database, if they don't already exist.
	"""
	db = lcl_connect()
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
				   INSERT INTO users (name, display_name, password) 
				   VALUES (?, ?, ?)
				   ''', (name, display_name, password))
	
	db.commit()
	db.close()
	print(f"User {name} added to the database.")
	return True

def get_hashed_password(user) -> str | None:
	"""
	Retrieves the hashed password for a user from the database.
	"""
	db = lcl_connect()
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
	db = lcl_connect()
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
	

	db = lcl_connect()
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

def sql_create_note(user, note) -> None:
	"""
	Creates a note in the database.
	"""
	db = lcl_connect()
	cursor = db.cursor()
	
	cursor.execute('''
				   SELECT notes FROM users WHERE name = ?
				   ''', (user,))
	result = cursor.fetchone()
	if result and result[0] is not None:
		notes = result[0] + ";;;" + note
		note = notes
	
	cursor.execute('''
				   UPDATE users SET notes = ? WHERE name = ?
				   ''', (note, user))
	
	db.commit()
	db.close()
	print("Note created in the database.")

	print("Printing entire database:")

	db = lcl_connect()
	cursor = db.cursor()
	cursor.execute('''
				   SELECT * FROM users
				   ''')
	data = cursor.fetchall()
	
	# Close the database connection
	db.close()
	if not data:
		print("No data found in the database.")
		return
	for row in data:
		print(row)

def sql_get_notes(user) -> list[str]:
	"""
	Retrieves notes for a user from the database.
	"""
	db = lcl_connect()
	cursor = db.cursor()
	
	cursor.execute('''
				   SELECT notes FROM users WHERE name = ?
				   ''', (user,))
	result = cursor.fetchone()
	db.close()
	
	if result and result[0] is not None:
		return result[0].split(";;;")
	else:
		return []

if __name__ == "__main__":
	import sys
	if sys.flags.interactive:
		print("Running in interactive mode.")
		sql_set_up()
		print("SQLite database setup complete.")
		print("Creating object 'test' of SQLiteHandler class.")
		# Check if we are in interactive mode

		test = SQLiteHandler()
	
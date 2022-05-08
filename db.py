import sqlite3
from abc import ABC, abstractmethod

con = sqlite3.connect('shop_list.db')
cur = con.cursor()

class BaseAbstractDb(ABC):
	querys = []
	@abstractmethod
	def save(self):
		pass

	@abstractmethod
	def get(self):
		pass

	@abstractmethod
	def all(self):
		pass

	@abstractmethod
	def delete(self):
		pass

class BaseDb(BaseAbstractDb):
	querys = []
	table_name = ""
	def __init__(self,**kwargs):
		sql = "INSERT INTO "+self.table_name
		sql += " ("
		for i in range(len(self.querys)):
			sql += "'"+ str(self.querys[i])+"'"
			if len(kwargs)>i+1:sql += ", "

		sql += ") VALUES ("
		for i in range(len(self.querys)):
			val = kwargs.get(self.querys[i])
			if val:sql += "'"+ str(val)+"'"
			if len(kwargs)>i+1:sql += ", "
		sql += ");"
		cur.execute(sql)

	@classmethod
	def get(cls,**kwargs):
		sql = "SELECT * FROM "+cls.table_name+" WHERE "
		for i in range(len(cls.querys)):
			val = kwargs.get(cls.querys[i])
			if val:sql += str(cls.querys[i])+" = '"+str(val)+"'"
			if len(kwargs)>i+1:sql += " AND "
		sql += ";"
		return cur.execute(sql).fetchall()

	def save(self):
		con.commit()

	@classmethod
	def all(cls):
		return cur.execute("SELECT * FROM "+cls.table_name+"").fetchall()

	@classmethod
	def delete(cls,**kwargs):
		sql = "DELETE FROM "+cls.table_name+" WHERE "
		for i in range(len(cls.querys)):
			val = kwargs.get(cls.querys[i])
			if val:sql += str(cls.querys[i])+" = '"+str(val)+"'"
			if len(kwargs)>i+1:sql += " AND "
		sql += ";"
		cur.execute(sql)
		con.commit()



class User(BaseDb):
	querys = ["name","telegram_id"]
	table_name = "users"

class Type(BaseDb):
	querys = ["id","type"]
	table_name = "types"

class Shop(BaseDb):
	querys = ["name","type","user"]
	table_name = "shops"


# def create_db():
# 	cur.execute('''CREATE TABLE users (
# 			name TEXT NOT NULL,
# 			telegram_id INTEGER NOT NULL UNIQUE
# 		);''')

# 	cur.execute('''CREATE TABLE types (
# 			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 			type TEXT NOT NULL UNIQUE
# 		);''')

# 	cur.execute('''CREATE TABLE shops (
# 			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 			name TEXT NOT NULL,
# 			type INTEGER,
# 			user INTEGER,
# 			FOREIGN KEY (type)
# 			REFERENCES types(id),
# 			FOREIGN KEY (user)
# 			REFERENCES users(telegram_id)
# 		);''')
	
# 	cur.execute("INSERT INTO types (type) VALUES ('Necerrasy')")
# 	cur.execute("INSERT INTO types (type) VALUES ('Need')")
# 	cur.execute("INSERT INTO types (type) VALUES ('Unimportant')")

# 	print(cur.execute("SELECT * FROM types").fetchall())
# 	con.commit()

# create_db()
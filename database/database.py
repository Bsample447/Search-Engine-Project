import sqlite3

connection = sqlite3.connect("linux_distro.db")

cursor = connection.cursor()

cursor.execute("create table linux (Distribution, " + ",".join(column_names)+ ")")
for i in range(len(df)):
	cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)",
	
connection.commit()

connection.close()
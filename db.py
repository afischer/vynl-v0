import sqlite3
def addUnique(key):  # Adds unique key to uniques database, and creates a database with a unique name
	conn = sqlite3.connect('uniques.db')
	c=conn.cursor()
	key=(key,)
	try:
		c.execute("CREATE TABLE unique (url TEXT, active BOOLEAN)")
	except:
		pass
	conn2=sqlite3.connect(key[0]+".db")
	c2=conn2.cursor()
	c2.execute("CREATE TABLE songs (videoid TEXT, upvotes REAL,downvotes REAL, name TEXT, artist TEXT, albumart TEXT)")
	conn2.commit()
	conn2.close()
	c.execute("INSERT INTO unique (url) VALUES (?)", key)
	conn.commit()
	conn.close()
def addSong(key,url):
	try:
		conn=sqlite3.connect(key+'.db')
	except:
		print "key does not exist"
	c=conn.cursor()
	

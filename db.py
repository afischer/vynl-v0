import sqlite3
import musicbrainzngs as mz
def addUnique(key):  # Adds unique key to uniques database, and creates a database with a unique name
	conn = sqlite3.connect('uniques.db')
	c=conn.cursor()
	key=(key,)
	try:
		c.execute("CREATE TABLE unique (url TEXT, active INTEGER)")
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

def addSong(key,vid,image):
	try:
		conn=sqlite3.connect(key+'.db')
	except:
		print "This party does not exist"
		return -1
	args=(vid,image,)
	c=conn.cursor()
	c.execute("INSERT INTO songs (videoid,albumart) VALUES (?,?)",args)
	conn.commit()
	conn.close()
	
	
	
	

import sqlite3
def addUnique(key):
	conn = sqlite3.connect('uniques.db')
	c=conn.cursor()
	key=(key,)
	try:
		c.execute("CREATE TABLE unique (url text)",key)
	except:
		pass


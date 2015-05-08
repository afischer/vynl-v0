import sqlite3
import musicbrainzngs as mz
class Party:
	def __init__(self,key):  # Adds unique key to uniques database, and creates a database with a unique name
		self.k=key
		self.db=self.k+'.db'
		conn = sqlite3.connect('uniques.db')
		c=conn.cursor()
		try:
			c.execute("CREATE TABLE unique (url TEXT, active INTEGER)")
		except:
			pass
		conn2=sqlite3.connect(self.db)
		c2=conn2.cursor()
		c2.execute("CREATE TABLE songs (videoid TEXT, upvotes REAL,downvotes REAL, name TEXT, artist TEXT, albumart TEXT)")
		conn2.commit()
		conn2.close()
		c.execute("INSERT INTO unique (url) VALUES (?)", (self.k,))
		conn.commit()
		conn.close()

	def addSong(self,vid,image):
		conn=sqlite3.connect(self.db)
		args=(vid,image,)
		c=conn.cursor()
		c.execute("INSERT INTO songs (videoid,albumart) VALUES (?,?)",args)
		conn.commit()
		conn.close()
	
	def upVote(self,vid):
		conn=sqlite3.connect(self.db)
		c=conn.cursor()
		num=c.execute("SELECT upvotes FROM songs WHERE videoid=?",(vid,))
		num+=1
		c.execute("INSERT INTO songs (upvotes) VALUES (?) WHERE videoid=?",(num,),(vid,))
		conn.commit()
		conn.close()

    	def downVote(self,vid):
        	conn=sqlite3.connect(self.db)
        	c=conn.cursor()
        	num=c.execute("SELECT downvotes FROM songs WHERE videoid=?",(vid,))
        	num+=1
        	c.execute("INSERT INTO songs (downvotes) VALUES (?) WHERE videoid=?",(num,),(vid,))
        	conn.commit()
		conn.close()

	
	
	

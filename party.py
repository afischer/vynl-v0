import sqlite3,os
import json as j
class Party:
	def __init__(self,key):  # Adds unique key to uniques database, and creates a database with a unique name
		self.k=key
		self.db=self.k+'.db'
		conn = sqlite3.connect('uniques.db')
		c=conn.cursor()
		try:
			c.execute("CREATE TABLE uniques (url TEXT, active INTEGER)")
		except:
			pass
		self.active=len(c.execute("SELECT (url) FROM uniques WHERE url=? AND active=1",(self.k,)).fetchall())
		if (self.active):
			conn.close()
			return 
		conn2=sqlite3.connect(self.db)
		c2=conn2.cursor()
		c2.execute("CREATE TABLE songs (videoid TEXT, upvotes REAL,downvotes REAL, name TEXT, artist TEXT, active INTEGER,total REAL)")
		conn2.commit()
		conn2.close()
		c.execute("INSERT INTO uniques (url,active) VALUES (?,?)", (self.k,1,))
		conn.commit()
		conn.close()
		self.active=True

	def addSong(self,vid,title,artist):
		if self.active:
			conn=sqlite3.connect(self.db)
			args=(vid,1,title,artist,)
			c=conn.cursor()
			c.execute("INSERT INTO songs (videoid,active,name,artist,upvotes,downvotes,total) VALUES (?,?,?,?,0,0,0)",args)
			conn.commit()
			conn.close()
		else:
			print "Party not active."
			return -1
	
	def removeSong(self,vid):
		if self.active:
			conn=sqlite3.connect(self.db)
			c=conn.cursor()
			c.execute("INSERT INTO songs (active) VALUES (?) WHERE videoid=?",(0,),(vid,))
			conn.commit()
			conn.close()
		else:
			print "Party not active."
			return -1
	def upVote(self,vid):
		if self.active:
			conn=sqlite3.connect(self.db)
			c=conn.cursor()
			num=c.execute("SELECT upvotes,total FROM songs WHERE videoid=?",(vid,)).fetchone()
			c.execute("UPDATE songs SET upvotes=?, total=? WHERE videoid=?",(num[0]+1,num[1]+1,vid,))
			conn.commit()
			conn.close()
		else:
			print "Party not active."
			return -1


   	def downVote(self,vid):
		if self.active:
			conn=sqlite3.connect(self.db)
			c=conn.cursor()
			num=c.execute("SELECT downvotes,total FROM songs WHERE videoid=?",(vid,)).fetchone()
			c.execute("UPDATE songs SET downvotes=?,total=? WHERE videoid=?",(num[0]+1,num[1]-1,vid,))
			conn.commit()
			conn.close()
		else:
			print "Party not active."
			return -1

	def end(self):
		if self.active:
			os.system('rm "'+self.db+'"')
			self.active=False
			conn = sqlite3.connect('uniques.db')
			c=conn.cursor()
			c.execute("UPDATE uniques SET active=? WHERE url=?",(0,self.k,))
			conn.commit()
			conn.close()


	def getOrdered(self): #{title: STRING, artist:STRING, videoID: STRING, upvotes: int, downvotes: int}
		if self.active:
			ret=[]
			conn=sqlite3.connect(self.db)
			c=conn.cursor()
			it=c.execute("SELECT name,artist,videoid, upvotes, downvotes FROM songs WHERE active=1 ORDER BY total DESC").fetchall()
			conn.close()
			for x in it:
					ret.append({"title":str(x[0]),"artist":str(x[1]),"videoID":str(x[2]),"upvotes":x[3],"downvotes":x[4]})
			return ret

	

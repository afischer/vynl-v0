import sqlite3
import os


class Party:
    # Adds unique key to uniques database and creates a database with a name
    def __init__(self, key):
        self.k = key
        self.db = 'parties.db'
        conn = sqlite3.connect('parties.db')
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE uniques (url TEXT, active INTEGER)")
        except:
            pass
        self.active=len(c.execute("SELECT (url) FROM uniques WHERE url=? AND active=1",(self.k,)).fetchall())
        if (self.active):
            conn.close()
            return
        #conn2=sqlite3.connect(self.db)
        #c2=conn2.cursor()
        c.execute("CREATE TABLE ? (videoid TEXT, imgURL TEXT, upvotes REAL, downvotes REAL, name TEXT, artist TEXT, active INTEGER,total REAL)",(self.k,))
        conn.commit()
        c.execute("INSERT INTO uniques (url,active) VALUES (?,?)", (self.k,1,))
        conn.commit()
        conn.close()
        self.active=True

    def addSong(self,vid,imgURL,title,artist):
        if self.active:
            conn=sqlite3.connect(self.db)
            args=(vid,imgURL,1,title,artist,)
            c=conn.cursor()
            c.execute("INSERT INTO ? (videoid,imgURL,active,name,artist,upvotes,downvotes,total) VALUES (?,?,?,?,?,0,0,0)",(self.k,),args)
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1

    def removeSong(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            c.execute("INSERT INTO ? (active) VALUES (?) WHERE videoid=?",(self.k,),(0,),(vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1
    def upVote(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT upvotes,total FROM ? WHERE videoid=?",(self.k,),(vid,)).fetchone()
            c.execute("UPDATE ? SET upvotes=?, total=? WHERE videoid=?",(self.k,),(num[0]+1,num[1]+1,vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1


    def downVote(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT downvotes,total FROM ? WHERE videoid=?",(self.k,),(vid,)).fetchone()
            c.execute("UPDATE ? SET downvotes=?,total=? WHERE videoid=?",(self.k,),(num[0]+1,num[1]-1,vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1

    def end(self):
        if self.active:
            #os.system('rm "'+self.db+'"')
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
            it=c.execute("SELECT name,artist,videoid,imgURL, upvotes, downvotes FROM songs WHERE active=1 ORDER BY total DESC").fetchall()
            conn.close()
            for x in it:
                ret.append({"songname":str(x[0]),"songartist":str(x[1]),"songID":str(x[2]),"albumarturl":str(x[3]),"upvotes":x[4],"downvotes":x[5]})
            return ret



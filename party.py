import sqlite3
import os

def scrub(query):
    return ''.join(x for x in query if x.isalnum())

class Party:
    # Adds unique key to uniques database and creates a database with a name
    def __init__(self, key, dj=0):
        self.k = scrub(key)
        #print self.k
        self.db = 'parties.db'
        conn = sqlite3.connect('parties.db')
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE uniques (url TEXT, active INTEGER)")
        except:
            pass
        self.active= len(c.execute("SELECT (url) FROM uniques WHERE url=? AND active=1",(self.k,)).fetchall())
        #print self.active
        if (self.active):
            #print dj
            self.dj=c.execute("SELECT ip FROM djs WHERE party=?",(self.k,)).fetchall()[0]
            #print self.dj
            conn.close()
            return
        #print "why"
        #conn2=sqlite3.connect(self.db)
        #c2=conn2.cursor()
        c.execute("CREATE TABLE " + self.k +"(videoid TEXT, imgURL TEXT, upvotes REAL, downvotes REAL, name TEXT, artist TEXT, active INTEGER,total REAL)")
        conn.commit()
        self.addDJ(dj)
        c.execute("INSERT OR REPLACE INTO uniques (url,active) VALUES (?,?)", (self.k,1,))
        conn.commit()
        conn.close()
        self.dj=dj
        self.active=True

    def addSong(self,vid,imgURL,title,artist):
        if self.active:
            conn=sqlite3.connect(self.db)
            args=(vid,imgURL,1,title,artist,)
            c=conn.cursor()
            c.execute("INSERT INTO "+self.k+ "(videoid,imgURL,active,name,artist,upvotes,downvotes,total) VALUES (?,?,?,?,?,0,0,0)",args)
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1

    def removeSong(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            c.execute("INSERT INTO "+self.k+ "(active) VALUES (?) WHERE videoid=?",(0,),(vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1
    def upVote(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT upvotes,total FROM "+self.k+" WHERE videoid=?",(vid,)).fetchone()
            c.execute("UPDATE "+self.k+" SET upvotes=?, total=? WHERE videoid=?",(num[0]+1,num[1]+1,vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1


    def downVote(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT downvotes,total FROM "+self.k+" WHERE videoid=?",(vid,)).fetchone()
            c.execute("UPDATE "+self.k+" SET downvotes=?,total=? WHERE videoid=?",(num[0]+1,num[1]-1,vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1

    def end(self):
        if self.active:
            #os.system('rm "'+self.db+'"')
            self.active=False
            conn = sqlite3.connect('parties.db')
            c=conn.cursor()
            c.execute("UPDATE uniques SET active=? WHERE url=?",(0,self.k,))
            c.execute("DROP TABLE "+self.k)
            conn.commit()
            conn.close()


    def getOrdered(self): #{title: STRING, artist:STRING, videoID: STRING, upvotes: int, downvotes: int}
        if self.active:
            ret=[]
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            it=c.execute("SELECT name,artist,videoid,imgURL, upvotes, downvotes FROM "+self.k+" WHERE active=1 ORDER BY total DESC").fetchall()
            conn.close()
            for x in it:
                ret.append({"songname":str(x[0]),"songartist":str(x[1]),"songID":str(x[2]),"albumarturl":str(x[3]),"upvotes":x[4],"downvotes":x[5]})
            return ret
    def addDJ(self,dj):
        conn=sqlite3.connect(self.db)
        c=conn.cursor()
        try:
            c.execute("CREATE TABLE djs (party TEXT, ip TEXT)")
        except:
            pass
        c.execute("INSERT INTO djs(party, ip) VALUES (?,?)",(self.k,dj,))
        conn.commit()
        conn.close()
        #print "ayy"

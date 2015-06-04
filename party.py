import sqlite3
import os
import marshal as m
##added a comment to test broken commits
def partyExists(key):
    try:
        conn = sqlite3.connect('parties.db')
        c = conn.cursor()
        n=len(c.execute("SELECT * FROM uniques WHERE url=? AND active=1",(key,)))
        return n>0
    except:
        return False

def scrub(query):
    return "["+''.join(x for x in query if x.isalnum())+"]"

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
            self.dj=c.execute("SELECT ip FROM djs WHERE party=?",(self.k,)).fetchall()[0][0]
            #print self.dj
            conn.close()
            return
        #print "why"
        #conn2=sqlite3.connect(self.db)
        #c2=conn2.cursor()
        c.execute("CREATE TABLE " + self.k +"(videoid TEXT, imgURL TEXT, upvotes REAL, downvotes REAL, name TEXT, artist TEXT, active INTEGER,total REAL, upvoteip BLOB, downvoteip BLOB)")
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
            x=m.dumps([])
            y=m.dumps([])
            args=(vid,imgURL,1,title,artist,x,y,)
            c=conn.cursor()
            c.execute("INSERT INTO "+self.k+ "(videoid,imgURL,active,name,artist,upvotes,downvotes,total,upvoteip,downvoteip) VALUES (?,?,?,?,?,0,0,0,?,?)",args)
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1

    def removeSong(self,vid):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            c.execute("UPDATE "+self.k+ "SET active = 0 WHERE videoid=?",(vid,))
            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1
    def upVote(self,vid, ip):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT upvotes,total,upvoteip, downvotes, downvoteip FROM "+self.k+" WHERE videoid=?",(vid,)).fetchone()
            x=m.loads(num[2])
            y=m.loads(num[4])
            if ip not in x:
                if ip in y:
                    x.append(ip)
                    y.remove(ip)
                    x=m.dumps(x)
                    y=m.dumps(y)
                    c.execute("UPDATE "+self.k+" SET upvotes=?, total=?, upvoteip=?, downvotes=?, downvoteip=? WHERE videoid=?",(num[0]+1,num[1]+2,x, num[3]-1,y,vid,))
                else:
                    x.append(ip)
                    x=m.dumps(x)
                    c.execute("UPDATE "+self.k+" SET upvotes=?, total=?, upvoteip=? WHERE videoid=?",(num[0]+1,num[1]+1,x,vid,))
            elif ip in x:
                x.remove(ip)
                x=m.dumps(x)
                c.execute("UPDATE "+self.k+" SET upvotes=?, total=?, upvoteip=? WHERE videoid=?",(num[0]-1,num[1]-1,x,vid,))

            conn.commit()
            conn.close()
        else:
            print "Party not active."
            return -1


    def downVote(self,vid, ip):
        if self.active:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            num=c.execute("SELECT downvotes,total,downvoteip, upvotes, upvoteip FROM "+self.k+" WHERE videoid=?",(vid,)).fetchone()
            x=m.loads(num[2])
            y=m.loads(num[4])
            if ip not in x:
                if ip in y:
                    x.append(ip)
                    y.remove(ip)
                    x=m.dumps(x)
                    y=m.dumps(y)
                    c.execute("UPDATE "+self.k+" SET downvotes=?, total=?, downvoteip=?, upvotes=?, upvoteip=? WHERE videoid=?",(num[0]+1,num[1]-2,x, num[3]-1,y,vid,))
                else:
                    x.append(ip)
                    x=m.dumps(x)
                    c.execute("UPDATE "+self.k+" SET downvotes=?, total=?, downvoteip=? WHERE videoid=?",(num[0]+1,num[1]-1,x,vid,))
            elif ip in x:
                x.remove(ip)
                x=m.dumps(x)
                c.execute("UPDATE "+self.k+" SET downvotes=?, total=?, downvoteip=? WHERE videoid=?",(num[0]-1,num[1]+1,x,vid,))

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


    def getOrdered(self,ip): #{title: STRING, artist:STRING, videoID: STRING, upvotes: int, downvotes: int}
        if self.active:
            ret=[]
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            it=c.execute("SELECT name,artist,videoid,imgURL, upvotes, downvotes,upvoteip,downvoteip FROM "+self.k+" WHERE active=1 ORDER BY total DESC").fetchall()
            conn.close()
            for x in it:
                ret.append({"songname":str(x[0]),"songartist":str(x[1]),"songID":str(x[2]),"albumarturl":str(x[3]),"upvotes":x[4],"downvotes":x[5],"upvoted":(ip in m.loads(x[6])), "downvoted":(ip in m.loads(x[7]))})
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

    def getDJ(self):
        if self.active:
            return self.dj

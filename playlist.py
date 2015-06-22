import party
def playlistExists(name):
    conn=sqlite3.connect('playlists.db')
    c=conn.cursor()
    try:
        exists=len(c.execute("SELECT * FROM names WHERE name=?",(name,)).fetchall())==1
    except:
        c.execute("CREATE TABLE names (name TEXT)")
        conn.commit()
        exists=False
    conn.close()
    return exists



class Playlist:
    def __init__(self, name):
        self.db='playlists.db'
        self.name=name
        exists=playlistExists(name)
        if not exists:
            conn=sqlite3.connect(self.db)
            c=conn.cursor()
            c.execute("INSERT INTO names (name) VALUES (?)",(name,))
            c.execute("CREATE TABLE "+name+" (videoid TEXT PRIMARY KEY ON DUPLICATE IGNORE, imgURL TEXT,name TEXT, artist TEXT)")
            conn.commit()
            conn.close()
    def addSong(self,vid,img,title,artist):
        conn=sqlite3.connect(self.db)
        c=conn.cursor()
        c.execute("INSERT INTO "+self.name+"(videoid,imgURL,name,artist) VALUES (?,?,?,?)",(vid,img,title,artist,))
        conn.commit()
        conn.close()

    def removeSong(self,vid):
        conn=sqlite3.connect(self.db)
        c=conn.cursor()
        c.execute("DELETE FROM "+self.name+ " WHERE videoid=?",(vid,))
        conn.commit()
        conn.close()

    def addParty(self,p):
        if not partyExists(p):
            return "Party does not exist."
        L=p.getSongs()


        c.executemany("INSERT INTO "+self.name+"(videoid,imgURL,name,artist)",L)
        conn.commit()
        conn.close()

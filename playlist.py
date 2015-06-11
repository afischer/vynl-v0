import party
db="playlists.db"
def saveParty(p,name):
    L=p.getSongs()
    conn=sqlite3.connect(db)
    c=conn.cursor()
    try:
        exists=len(c.execute("SELECT * FROM names WHERE name=?",(name,)).fetchall())
    except:
        c.execute("CREATE TABLE names (name TEXT)")
        conn.commit()
        exists=False
    if exists:
        conn.close()
        print "Name is in use."
        return -1
    c.execute("CREATE TABLE "+name+" (videoid TEXT PRIMARY KEY, imgURL TEXT,name TEXT, artist TEXT)")
    c.executemany("INSERT INTO "+name+"(videoid,imgURL,name,artist)",L)
    conn.commit()
    conn.close()

class Playlist:
    def __init__(self, name):

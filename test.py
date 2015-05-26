import party,os
#try:
x=party.Party("hey")
song="xxx5"
song2="yyy5"
song3="fff5"
song4="qqqqq"
x.addSong(song,"exampleimage","name","channelman")
x.addSong(song2,"exampleimage","name2","channelwhat")
x.addSong(song3,"exampleimage","name3","channelwho")
x.addSong(song4,"exampleimage","name4","itstaytay")
for i in xrange(20):
	x.upVote(song)
for i in xrange(10):
	x.downVote(song)
for i in xrange(13):
	x.upVote(song2)
for i in xrange(20):
	x.downVote(song3)
for i in xrange(30):
	x.downVote(song4)
for i in xrange(50):
	x.upVote(song4)

print x.getOrdered()
y=party.Party("hey")
print y.getOrdered()
x.end()
#except:
#	os.system("rm uniques.db;rm hey.db")

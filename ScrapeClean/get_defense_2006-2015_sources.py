import requests

for i in range(2006, 2016):
    for j in range(1,18):
        u = 'http://www.thehuddle.com/stats/%d/plays_weekly.php?week=%d&pos=df&col=FPTS' %(i, j)
        src = requests.get(u)
        with open('Data/Raw/HTML/DEF_%d_Wk%d.html' %(i, j), 'wb') as f:
            f.write(src.text)
        print "Wrote DEF Week %d, %d" %(j, i)

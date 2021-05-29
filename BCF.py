import zipfile
import re
from database import cursor,db
def add_log(text, user,date):
    sql = ("INSERT INTO BCFTABLE (Title,CreationAuthor,CreationDate) VALUES (%s, %s,%s)")
    cursor.execute(sql, (text, user,date))
    db.commit()
    log_id = cursor.lastrowid
    print("Added log {}".format(log_id))

def get_logs():
    sql = ("SELECT * FROM BCFTABLE")
    cursor.execute(sql)
    result = cursor.fetchall()

    for row in result:
        print(row[1])


Dtime=[]
XLIST=[]
Xtxt=[]
#Xcap='Title','Priority','Index','CreationDate','CreationAuthor','ModifiedDate','ModifiedAuthor','AssignedTo','Date','Author','Comment','ModifiedDate','ModifiedAuthor'
Title=[]
CreationDate=[]
CreationAuthor=[]
zip = zipfile.ZipFile('BCF.bcf')
XLIST=zip.namelist()

for i in XLIST:
    ext=i.split(".")
    if ext[-1]=="bcf":
        ixfile = str(zip.read(i),'utf-8')
        #Xtxt=re.split("[<>]",ixfile)
        Xtxt=ixfile.split("\n\t\t")
        for i2 in Xtxt:
            Xline=re.split("[<>]",i2)
            #print(Xline[1],":",Xline[2])

            if Xline[1]=="Title":
                Title.append(Xline[2])
            if Xline[1]=="CreationDate":
                Dtime=re.split("[T+]",Xline[2])
                CreationDate.append(Dtime[0]+" "+Dtime[1])
            if Xline[1]=="CreationAuthor":
                CreationAuthor.append(Xline[2])
                break
#print(Title)
#print(CreationAuthor)
#print(CreationDate)
i=0

for n in Title:
    add_log(n, CreationAuthor[i],CreationDate[i])
    i=i+1

#get_logs()
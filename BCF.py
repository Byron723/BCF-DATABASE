import xml.etree.ElementTree as ET
import mysql.connector
import zipfile
import itertools
config={
    'user':'root',
    'password': 'MqZ7vg0pmqkJ=',
    'host':'localhost',
    'database':'BIM'
}
db=mysql.connector.connect(**config)
cursor=db.cursor()

def add_log(ID,DATA,COLUM,TABLE,IDNAME): #Agregar nueva entrada
    sDATA=str(DATA)
    sID=str(ID)
    COLUM=str(COLUM)
    IDNAME=str(IDNAME)
    sql=("INSERT INTO "+TABLE+" ("+IDNAME+","+COLUM+") VALUE ('"+sID+"','"+sDATA+"')")
    cursor.execute(sql)
    db.commit()

def add_columSTR(COLUM,TABLE): #Crear Nueva Columna String
    sql="ALTER TABLE "+TABLE+" ADD "+COLUM+" VARCHAR (100)"
    cursor.execute(sql,(COLUM))
    db.commit()

def ID_Check(ID,TABLE): #Revisar si ID existe en SQL
    sql = ("SELECT * FROM "+TABLE)
    colum=[]
    cursor.execute(sql)
    data = cursor.fetchall()
    for n in data:
        colum.append(n[0])
    if str(ID) in colum:
        IDChek=True
    else:
        IDChek=False
    return IDChek

def get_logs():
    sql = ("SELECT * FROM PARAMETERS")
    colum=[]
    cursor.execute(sql)
    data = cursor.fetchall()
    for n in data:
        colum.append(n)
    return colum

def update_log(ID, DATA,COLUM,TABLE,IDNAME): #Actualizar entrada
    sql = str("UPDATE "+TABLE+" SET "+COLUM+" ='"+str(DATA)+"' WHERE "+IDNAME+" ='"+ID+"'")
    cursor.execute(sql)
    db.commit()

def Column_Check(COLUM,TABLE): #Revisar si columna existe
    sql = ("DESCRIBE "+TABLE)
    icolum=[]
    cursor.execute(sql)
    idata = cursor.fetchall()
    for n in idata:
        icolum.append(n[0])
    if str(COLUM) in icolum:
        CCheck=True
    else:
        CCheck=False
    return CCheck

def update_table(ID,DATA,COLUM,TABLE,IDNAME):
    if Column_Check(COLUM,TABLE):
        if ID_Check(ID,TABLE):
            update_log(ID,DATA,COLUM,TABLE,IDNAME)
        else:
            add_log(ID,DATA,COLUM,TABLE,IDNAME)
    else:
        add_columSTR(COLUM,TABLE)
        if ID_Check(ID,TABLE):
            update_log(ID,DATA,COLUM,TABLE,IDNAME)
        else:
            add_log(ID,str(DATA),COLUM,TABLE,IDNAME)

def dataL(list,data): #Corregir campos repedidas 
    if (data not in list):
        list.append(data)
    else:
        for n in range(2,10):
            if (data+str(n)) not in list:
                list.append(data+str(n))
                break
    return list

def interate_table(COLUM,DATA):
    ID=DATA[0]
    IDNAME=COLUM[0]
    TABLE="BCFTABLE"
    for x in range(1,len(COLUM)):
        update_table(ID,DATA[x],COLUM[x],TABLE,IDNAME)

zip = zipfile.ZipFile('BCF.bcf')
XLIST=zip.namelist()
for i in XLIST:
    ext=i.split(".")
    if ext[-1]=="bcf":
        ixfile = zip.open(i)
        tree=ET.parse(ixfile)
        root=tree.getroot()
        Child=[]
        Tdata=[]
        XID=[]
        for elem in root.findall("*"):
            try:
                Child.append(elem.tag)
                for N0 in list(elem.attrib):
                    dataL(XID,N0)
                for N0 in list(elem.attrib.values()):
                    Tdata.append(str(N0))
            except:
                pass
        for n in Child:
            txChild="./"+str(n)+"/"
            for elem in root.findall(txChild):
                try:
                    Tdata.append(elem.text)
                    Cdat=n+"_"+elem.tag
                    dataL(XID,Cdat)
                except:
                    pass
            interate_table(XID,Tdata)
        print(XID[0]+" "+Tdata[0])
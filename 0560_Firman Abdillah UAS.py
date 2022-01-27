from unittest import result
from urllib import response
import requests
from tabulate import tabulate
from mysql import connector

db = connector.connect(
    host    = 'localhost',
    user    = 'root',
    passwd  = '',
)
def createDatabase():
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE db_akademik_0560")


db = connector.connect(
    host    = 'localhost',
    user    = 'root',
    passwd  = '',
    database= 'db_akademik_0560'
)

def getDataEndpoint(endpoint):
    base_url = "https://api.abcfdab.cfd/"
    response = requests.get(base_url + endpoint)
    return response.json()


dataRaw = getDataEndpoint('students')
data_data = dataRaw['data']
dataCol = []
dataList = []
for d in data_data:
    for k,v in d.items():
        dataList.append(v)
        dataCol.append(k)
lmt=0
listDataRaw = []
while lmt<len(dataList):
    listDataRaw.append(dataList[lmt:lmt+6])
    lmt+=6

col=dataCol[1:6]

def createTbl():
    head1 = dataCol[0]
    mycursor = db.cursor()
    mycursor.execute(f"CREATE TABLE tbl_students_0560 ({head1} int)")
    for t in col:
        mycursor.execute(f"ALTER TABLE tbl_students_0560 ADD {t} varchar(255);")
    
def adddataSQL():
    mycursor = db.cursor()
    for d in listDataRaw:
        q= tuple(d)
        mycursor.execute('INSERT INTO tbl_students_0560 (id, nim, nama, jk, jurusan, alamat) VALUES (%s,%s,%s,%s,%s,%s)', q ),
    db.commit() 

listColumn=[]
dataListFinal = []
def getdata():
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM tbl_students_0560")
    myresult = mycursor.fetchall()
    listData=[]
    for i in myresult:
        for k in i:
            listData.append(k)

    i=0
    while i<len(listData):
        dataListFinal.append(dataList[i:i+6])
        i+=6

def getColumn():
    mycursor = db.cursor()
    mycursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='db_akademik_0560' AND `TABLE_NAME`='tbl_students_0560';")
    myresult = mycursor.fetchall()
    column = []
    for i in myresult:
        for k in i:
            column.append(k)
    for i in range(len(column)):
        column[i] = column[i].upper()
    listColumn.append(column)

getdata()
getColumn()

finalData = listColumn + dataListFinal

def showData():
    print(tabulate(finalData, headers='firstrow', tablefmt='grid'))

def basedLimit():
    limit=int(input('Massukkan limit: '))
    dataLimit = finalData[0:limit+1]
    print(tabulate(dataLimit, headers='firstrow', tablefmt='grid'))

def searchNim():
    nim = str(input('Masukkan NIM: '))
    for dl in dataListFinal:
        check = nim in dl
        if check == True:
            reslt = dl
            res = 'found'
        else:
            res = 'none'
            
    if res == 'found':
        reslist = []
        reslist.append(reslt)
        dataBasedNim = listColumn + reslist
        print('$ DATA DITEMUKAN $')
        print(tabulate(dataBasedNim, headers='firstrow', tablefmt='grid'))
    
    else:
        mess = ['NA']
        empty =[]
        empty6 = mess*6
        empty.append(empty6)
        emptyFinal = listColumn + empty
        print('$$ DATA TIDAK DITEMUKAN $$')
        print(tabulate(emptyFinal, headers='firstrow', tablefmt='grid'))
    
def menu():
    menu = int(input('''1. Tampilkan semua data
2. Tampilkan data berdasarkan limit
3. Cari data berdasarkan NIM
0. Keluar
Pilih menu> '''))

    if menu == 1:
        showData()
    elif menu == 2:
        basedLimit()
    elif menu == 3:
        searchNim()
    elif menu == 0:
        exit()
    else:
        print('Masukkan pilihan yang benar')

while True:
    menu()
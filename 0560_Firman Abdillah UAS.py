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
def createDB():
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


data = getDataEndpoint('students')
data_data = data['data']
dataHead = []
dataList = []
for d in data_data:
    for k,v in d.items():
        dataList.append(v)
        dataHead.append(k)
i=0
newLists = []
while i<len(dataList):
    newLists.append(dataList[i:i+6])
    i+=6

head=dataHead[1:6]

def createTB():
    head1 = dataHead[0]
    mycursor = db.cursor()
    mycursor.execute(f"CREATE TABLE tbl_students_0560 ({head1} int)")
    for t in head:
        mycursor.execute(f"ALTER TABLE tbl_students_0560 ADD {t} varchar(255);")
    
def adddata():
    mycursor = db.cursor()
    for d in newLists:
        q= tuple(d)
        mycursor.execute('INSERT INTO tbl_students_0560 (id, nim, nama, jk, jurusan, alamat) VALUES (%s,%s,%s,%s,%s,%s)', q ),
    db.commit() 

columnList=[]
dataLists = []
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
        dataLists.append(dataList[i:i+6])
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
    columnList.append(column)

getdata()
getColumn()

dataFinal = columnList + dataLists

def showData():
    print(tabulate(dataFinal, headers='firstrow', tablefmt='grid'))

def basedLimit():
    limit=int(input('Massukkan limit: '))
    dataLimit = dataFinal[0:limit+1]
    print(tabulate(dataLimit, headers='firstrow', tablefmt='grid'))

def cariNim():
    nim = str(input('Masukkan NIM: '))
    for p in dataFinal:
        check = nim in p
        if check == True:
            resList = p
            res = 'ada'
        else:
            res = 'none'
            
    if res == 'ada':
        hasil = []
        hasil.append(resList)
        dataBasedNim = columnList + hasil
        print(tabulate(dataBasedNim, headers='firstrow', tablefmt='grid'))
    
    else:
        empty = [['DATA TIDAK DITEMUKAN']]
        print(tabulate(empty, headers='firstrow', tablefmt='grid'))\
    
def menu():
    menu = int(input('''
    1. Tampilkan semua data
    2. Tampilkan data berdasarkan limit
    3. Cari data berdasarkan NIM
    0. Keluar
    Pilih menu> '''))

    if menu == 1:
        showData()
    elif menu == 2:
        basedLimit()
    elif menu == 3:
        cariNim()
    elif menu == 0:
        exit()
    else:
        print('Masukkan pilihan yang benar')

while True:
    menu()
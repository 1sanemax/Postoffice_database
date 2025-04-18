import csv
import os
import mysql.connector as sql

database = sql.connect(
    host = 'localhost',
    user = '**',#replace with your username
    passwd = '**',#replace with your password
)

cursor = database.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS sample_import')
cursor.execute('USE sample_import')

os.chdir('D:/SEM6/DATASCIENCE/MINIPROJ/Regions and Pincodes/Pincodes and Regions')
contents = os.listdir()

for name in contents:
    f = open(name, 'r', newline='')
    read = csv.reader(f)

    name = name[:-4:]
    print(name)

    statement = 'CREATE TABLE IF NOT EXISTS {} (SNO int, Region varchar(120), Pincodes int);'.format(name)
    cursor.execute(statement)

    flag_var = True
    for j in read:
        if flag_var:
            flag_var = False
            continue

        try:
            statement = 'INSERT INTO {}(SNO, Region, Pincodes) VALUES ({}, "{}", "{}");'.format(name, j[0], j[1], j[2])
            cursor.execute(statement)

        except IndexError:
            continue

    f.close()

database.commit()
database.close()

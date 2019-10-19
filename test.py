import pymysql

host = '39.108.125.89'
user = 'root'
password = 'qwe123'
database = 'Mail'

sql = 'select * from df_index_type_goods'
coon = pymysql.connect(host, user, password, database, 3306)
cursor = coon.cursor()
r = cursor.execute(sql)
result = []
for i in cursor.fetchall():
    item = []
    item.append(i[0])
    item.append(i[4])
    item.append(i[5])
    item.append(i[6])
    item.append(i[7])
    result.append(item)
coon.close()
# print(result)
host = '127.0.0.1'
user = 'root'
password = 'qwe123'
database = 'flask-env'
print(result[0][3])
coon = pymysql.connect(host, user, password, database, 3306)
cursor = coon.cursor()
for i in result:
    sql = "insert into df_index_type_goods(" \
          "`id`, display_type, `index`, sku, `type`" \
          ") values {}".format(tuple(i))

    print(sql)
    cursor.execute(sql)
coon.commit()
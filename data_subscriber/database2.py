import pymysql
#import charts
# 資料庫設定
def insert(token):
    db_settings = {
        "host": "mysql",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "rabbitmqdata",
        "charset": "utf8"
    }
    try:
    # 建立Connection物件
        conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
        with conn.cursor() as cursor:
      #資料表相關操作
            qmarks = ', '.join(['%s'] * len(token))
            columns = ', '.join(token.keys())
            command = "INSERT INTO customer(%s)VALUES(%s);" % (columns, qmarks)
            cursor.execute(command, token.values())
            conn.commit()
    except Exception as ex:
        print(ex)
#insert("123")

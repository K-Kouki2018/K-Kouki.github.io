import sqlite3

#データベース名(〇〇.db)
DB_Name = ("test.db") 

#データベース作成 自動コミット機能オプションON(自動上書き保存)
conn = sqlite3.connect(DB_Name, isolation_level=None)

#------------------------------------------------------------------------- テーブル作成

#sqliteを操作するカーソルオブジェクト作成
cursor = conn.cursor()

#executeコマンドでSQL実行(testというtableを作成)
sql = """CREATE TABLE IF NOT EXISTS test(id, name, date)"""
cursor.execute(sql)
#データベースにコミット(上書き保存)
conn.commit()

#table名の取得文
sql = """SELECT name FROM sqlite_master WHERE TYPE='table'"""

#for文で作成した全テーブルをターミナル出力確認
for t in cursor.execute(sql):
    print(t)

#------------------------------------------------------------------------- レコード格納準備

#レコード追加にINSERT文を使う
#レコード：行ごとのデータのこと
#SQLインジェクションという不正SQL命令への脆弱性対策でpythonの場合は「?」を使用して記載するのが基本。
#SQLインジェクション：Webアプリケーションの入力処理の不備を突き、不正なSQL文を実行させて
#                   データベース内の情報を取得・改ざん・削除するサイバー攻撃手法
#「?」は後で値を受け取るという意味
sql = """INSERT INTO test VALUES(?,?,?)"""

#------------------------------------------------------------------------- レコード１行格納
#挿入レコード指定(一行追加)

data = ((0,'Taro', 20000101))

cursor.execute(sql, data)
conn.commit()

print("レコード１行格納確認")
print(data)

#------------------------------------------------------------------------- レコード複数行格納
#挿入レコード指定(複数行追加)

data = [
    (1, "A_san", 20000101),
    (2, "B_san", 20000201),
    (3, "C_san", 20000301),
    (4, "D_san", 20000401),
    (5, "E_san", 20000501),
]

cursor.executemany(sql, data)#複数データの追加には「executemany」
conn.commit()

print("レコード複数行格納")
print(data)

#------------------------------------------------------------------------- 選択したテーブルから全レコードを取り出す
# select * ですべてのデータを参照、 from でどのテーブルからデータを呼ぶのか指定
# fetchall ですべての行のデータを取り出す

sql = """SELECT * FROM test"""

cursor.execute(sql)
#全レコードを取り出す
print("全レコード取り出し")
print(cursor.fetchall())

#------------------------------------------------------------------------- 選択したテーブルから１行ずつレコードを取り出す
#テーブルから１行ずつ取り出す
select_sql = """SELECT * FROM test"""
cursor.execute(select_sql)

print("全レコード１行ずつ取り出し")
while True:
    result = cursor.fetchone()#データを１行抽出
    if result is None :#抽出するデータがなくなったら
        break

    print(result)
#------------------------------------------------------------------------- 条件でレコードを削除
#whereのあとに削除したいデータの条件指定
#今回は例として id が 2 のデータを削除

cursor.execute('delete from test where id=?' ,(2,))
conn.commit()

cursor.execute('select * from test')
print("id=2のレコード削除")
print(cursor.fetchall())
#------------------------------------------------------------------------- テーブル名変更

sql = """ALTER TABLE test RENAME TO rename_test"""

conn.execute(sql)
conn.commit()

print("テーブル名変更")
sql = """SELECT name FROM sqlite_master WHERE TYPE='table'"""
for t in cursor.execute(sql):
     print(t)

#------------------------------------------------------------------------- テーブル削除
#今回は例として名前変更したテーブルを削除
sql = """DROP TABLE if exists rename_test"""

conn.execute(sql)
conn.commit()

#------------------------------------------------------------------------- 接続を遮断する

#作業完了したら接続を閉じる
cursor.close()
conn.close()
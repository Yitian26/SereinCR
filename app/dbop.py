import sqlite3


class DbOperation:
    @staticmethod
    def create():  # 创建数据库
        db = sqlite3.connect('Sereincr.db')
        print(db)
        cur = db.cursor()
        accountinf_sql = '''create table accountinf_sql(id varchar(50)  primary key,
                                                        name varchar(50),
                                                        password varchar(50),
                                                        lastlogin varchar(50)
                                                        )'''
        messages_sql = '''create table  messages_sql(id int,
                                                   time varchar(50),
                                                   sender varchar(50),
                                                   msg varchar(50)
                                                   )'''
        try:
            cur.execute(accountinf_sql)
            cur.execute(messages_sql)
        except Exception as error:
            print(error)
        finally:
            cur.close()
            db.close()

    @staticmethod  # 根据呢称查找
    def seekfromname(name, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("SELECT*FROM accountinf_sql WHERE name=?", [name])
        data = cur.fetchall()
        cur.close()
        db.close()
        return data

    @staticmethod  # 根据用户名查找
    def seekfromid(id, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        payload = "SELECT*FROM accountinf_sql WHERE id='{idd}'".format(idd=id)
        # print(payload)
        # cur.execute("SELECT*FROM accountinf_sql WHERE id=?", [id])
        cur.execute(payload)
        data = cur.fetchall()
        cur.close()
        db.close()
        return data

    @staticmethod  # 添加用户
    def addacc(data, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        insert_accountinf_sql = "insert into accountinf_sql(id,name,password,lastlogin)values(?,?,?,?)"
        try:
            cur.execute(insert_accountinf_sql, (data[0], data[1], data[2], data[3]))
            db.commit()
        except Exception as error:
            print(error)
            db.rollback()
        finally:
            cur.close()
            db.close()

    @staticmethod  # 更改信息
    def change(data, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        try:
            cur.execute("UPDATE accountinf_sql SET password = ?  WHERE id = ?", [data[1], data[0]])
            cur.execute("UPDATE accountinf_sql SET name = ?  WHERE id = ?", [data[2], data[0]])
            cur.execute("UPDATE accountinf_sql SET lastlogin = ?  WHERE id = ?", [data[3], data[0]])
            db.commit()
        except Exception as error:
            print(error)
            db.rollback()
        finally:
            cur.close()
            db.close()

    @staticmethod  # 删除用户
    def delacc(id, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("delete from accountinf_sql WHERE id = ?", [id])
        cur.close()
        db.commit()
        db.close()

    @staticmethod  # 判断数据库大小
    def dblength(dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("select id from accountinf_sql")
        data = cur.fetchall()
        cur.close()
        db.close()
        if len(data) != 0:
            if len(data[0]) == 100:
                return False
        return True

    @staticmethod  # 删除消息
    def delmsg(delall, data, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        if delall:
            cur.execute("delete from messages_sql WHERE id = ?", [data[0]])
        else:
            cur.execute("delete from messages_sql WHERE id = ? and time = ?", [data[0], data[1]])
        cur.close()
        db.commit()
        db.close()

    @staticmethod  # 添加消息
    def addmsg(data, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        insert_messages_sql = "insert into messages_sql(id,time,sender,msg)values(?,?,?,?)"
        try:
            cur.execute(insert_messages_sql, (data[0], data[1], data[2], data[3]))
            db.commit()
        except Exception as error:
            print(error)
            db.rollback()
        finally:
            cur.close()
            db.close()

    @staticmethod  # 查询消息
    def getmsgs(dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("SELECT * FROM messages_sql ORDER BY id desc limit 50")
        data = cur.fetchall()
        cur.close()
        db.close()
        return data

    @staticmethod  # 根据呢称查询消息
    def getmsgbyname(name, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("SELECT * FROM messages_sql WHERE sender = ? ORDER BY id desc limit 50", [name])
        data = cur.fetchall()
        cur.close()
        db.close()
        return data

    @staticmethod  # 自定义sql语句
    def executesql(strsql, dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute(strsql)
        data = cur.fetchall()
        if data:
            for x in data:
                print(x)
        del data
        cur.close()
        db.close()

    @staticmethod  # 查询所有账户
    def getaccounts(dbname):
        db = sqlite3.connect(dbname)
        cur = db.cursor()
        cur.execute("SELECT * FROM accountinf_sql ORDER BY id desc")
        data = cur.fetchall()
        cur.close()
        db.close()
        return data

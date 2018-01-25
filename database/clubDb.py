# -*- coding:utf-8 -*-
import pymysql
import configparser
#球队数据
class clubDb:
    #读取配置文件中的数据
    cf=configparser.ConfigParser()
    cf.read("database\\mitontteConf.conf","utf-8-sig")
    databaseName=cf.get("database","databaseName")
    host = cf.get("database","host")
    port = cf.getint("database","port")
    username = cf.get("database","username")
    password = cf.get("database","password")

    @staticmethod
    #连接数据库
    def __connectdb__():
        try:
            conn = pymysql.connect(host=clubDb.host, user=clubDb.username
                                   , passwd=clubDb.password, db=clubDb.databaseName, port=clubDb.port
                                   , charset='utf8')
            #创建一个数据库连接
            return conn
        except Exception:print("连接数据库失败！")

    @staticmethod
    # 创建数据表
    def createTeamTable():
        conn = clubDb.__connectdb__()
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = conn.cursor()
            # 使用 execute() 方法执行 SQL，如果表存在则删除
            cursor.execute("DROP TABLE IF EXISTS CLUB")
            # 使用预处理语句创建表
            sql = """CREATE TABLE CLUB(
                     CLUB_ID  INT PRIMARY KEY,
                     CLUB_NAME  VARCHAR(20) )"""
            cursor.execute(sql)
        except Exception:print("创建数据表失败！")
        # 关闭数据库连接
        finally:
            conn.close()
    @staticmethod
    def creatTeam(clubDict):
        conn = clubDb.__connectdb__()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''SELECT * from CLUB WHERE CLUB_ID = '%s' limit 1;
               ''' % (clubDict["id"])
        # 先判断俱乐部是否已经存在数据库中
        rowCount = 0
        info = dict()
        try:
            cursor.execute(sql)
            rowCount = cursor.rowcount
            info = cursor.fetchone()
        except Exception:
            print("创建新球队信息失败")
        finally:
            conn.close()
        #球队未被录入

        if rowCount == 0:
            conn = clubDb.__connectdb__()
            cursor = conn.cursor()
            sql = '''INSERT INTO CLUB (CLUB_ID,CLUB_NAME)
                       VALUES('%s','%s')''' % (clubDict["id"],clubDict["name"])
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception:
                # 发生错误，回滚数据库
                conn.rollback()
            finally:
                conn.close()
        #球队信息已经被录入

        else:
            # 更新
            conn =clubDb.__connectdb__()
            cursor = conn.cursor()
            sql = '''UPDATE CLUB SET CLUB_ID='%s',CLUB_NAME='%s'
                   ''' % (clubDict["id"],clubDict["name"])
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                # 发生错误，回滚数据库
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def queryUser(teamID):
        conn = clubDb.__connectdb__()
        cursor = conn.cursor()
        sql ='''SELECT * FROM CLUB USER_NUMBER="%s"'''%(teamID)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except:
            conn.rollback()
        finally:
            conn.close()
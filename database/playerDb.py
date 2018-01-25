# -*- coding:utf-8 -*-
import pymysql
import configparser
#球队数据
class playerDb:
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
            conn = pymysql.connect(host=playerDb.host, user=playerDb.username
                                   , passwd=playerDb.password, db=playerDb.databaseName, port=playerDb.port
                                   , charset='utf8')
            #创建一个数据库连接
            return conn
        except Exception:print("连接数据库失败！")

    @staticmethod
    # 创建数据表
    def createPlayersTable():
        conn = playerDb.__connectdb__()
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = conn.cursor()
            # 使用 execute() 方法执行 SQL，如果表存在则删除
            cursor.execute("DROP TABLE IF EXISTS PLAYERS")
            # 使用预处理语句创建表
            sql = """
                     CREATE TABLE PLAYERS(
                     PLAYER_ID  INT PRIMARY KEY,
                     CLUB_ID  INT,
                     BLOCK_HEIGHT INT,
                     WEIGHT INT,
                     INTERNATION_COUNT INT,
                     SPIKE_HEIGHT INT,
                     TOTAL INT,
                     LOCAL_COUNT INT,
                     PHOTO varchar(100),
                     HEIGHT INT,
                     BIRTHDAY DATE,
                     ZH_NAME VARCHAR(10),
                     NUMBER INT,
                     POSITION VARCHAR(10)
                      )"""
            cursor.execute(sql)
        except Exception:print("创建数据表失败！")
        # 关闭数据库连接
        finally:
            conn.close()
    @staticmethod
    def creatPlayer(playerDict):
        conn = playerDb.__connectdb__()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = '''SELECT * from PLAYERS WHERE PLAYER_ID = '%s' limit 1;
               ''' % (playerDict["id"])
        # 先判断球员是否已经存在数据库中
        rowCount = 0
        info = dict()
        try:
            cursor.execute(sql)
            rowCount = cursor.rowcount
            info = cursor.fetchone()
        except Exception:
            print("创建新球员信息失败")
        finally:
            conn.close()
        #球员未被录入
        if rowCount == 0:
            conn = playerDb.__connectdb__()
            cursor = conn.cursor()
            sql = '''INSERT INTO PLAYERS (PLAYER_ID,CLUB_ID,BLOCK_HEIGHT,WEIGHT,INTERNATION_COUNT,SPIKE_HEIGHT,TOTAL,LOCAL_COUNT,PHOTO,HEIGHT,BIRTHDAY,ZH_NAME,NUMBER,POSITION)
                       VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (playerDict["id"],playerDict["club_team_id"],playerDict["block_height"],playerDict["weight"],playerDict["int_count"],playerDict["spike_height"],
            playerDict["total"],playerDict["local_count"],playerDict["photo"],playerDict["height"],playerDict["birthday"],playerDict["zh_name"],playerDict["number"],playerDict["position"])
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception:
                # 发生错误，回滚数据库
                conn.rollback()
            finally:
                conn.close()
        #球员已经被录入

        else:
            # 更新
            conn =playerDb.__connectdb__()
            cursor = conn.cursor()
            sql = '''UPDATE CLUB SET PLAYER_ID='%s',CLUB_ID='%s',BLOCK_HEIGHT='%s',WEIGHT='%s',INTERNATION_COUNT='%s',SPIKE_HEIGHT='%s',TOTAL='%s',LOCAL_COUNT='%s',PHOTO='%s',HEIGHT='%s',BIRTHDAY='%s',ZH_NAME='%s',NUMBER='%s',POSITION='%s'
                   ''' % (playerDict["id"],playerDict["club_id"],playerDict["block_height"],playerDict["weight"],playerDict["internation_count"],playerDict["spike_height"],
            playerDict["total"],playerDict["local_count"],playerDict["photo"],playerDict["height"],playerDict["birthday"],playerDict["zh_name"],playerDict["number"],playerDict["position"])
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                # 发生错误，回滚数据库
                conn.rollback()
            finally:
                conn.close()

    @staticmethod
    def queryPlayer(playerID):
        conn = playerDb.__connectdb__()
        cursor = conn.cursor()
        sql ='''SELECT * FROM PLAYERS PLAYER_ID="%s"'''%(playerID)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except:
            conn.rollback()
        finally:
            conn.close()
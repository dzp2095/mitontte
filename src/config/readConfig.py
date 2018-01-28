import os
import configparser
class readConfig:
    #读取数据库配置文件
    @staticmethod
    def readDatabaseConfig():
    # 获取文件的当前路径（绝对路径）
        cur_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(cur_path, 'mitontteConf.conf')
        conf = configparser.ConfigParser()
        conf.read(config_path,"utf-8-sig")
        databaseInfo=dict()
        databaseInfo["databaseName"]= conf.get("database", "databaseName")
        databaseInfo["host"] = conf.get('database', "host")
        databaseInfo["port"] = conf.getint("database", "port")
        databaseInfo["username"] = conf.get("database", "username")
        databaseInfo["password"] = conf.get("database", "password")
        return  databaseInfo
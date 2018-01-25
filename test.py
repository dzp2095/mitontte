# -*- coding:utf-8 -*-

from spider import getPlayerData
import database
if __name__ == "__main__":
    #初始化数据表(第一次测试使用后可以注释掉)
    database.initDB()
    getPlayerData.getPlayerDate.queryPlayer()

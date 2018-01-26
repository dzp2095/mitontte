# -*- coding:utf-8 -*-

#爬虫测试
import database
from src import spider

if __name__ == "__main__":
    #初始化数据表(第一次测试使用后可以注释掉)
    #database.initDB()
    spider.getPlayerData.queryPlayer()


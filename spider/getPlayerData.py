# -*- coding:utf-8 -*-

#读取球队信息以及球员信息，保存进数据库

from pyquery import PyQuery
import database
import urllib
import http.cookiejar
class getPlayerDate:
    header = {
        "User-Agent": "Mozilla/5.0(Windows NT 6.3; Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        "Content-Type": "application / x - www - form - urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    def __init__(self):
        return
    @staticmethod
    def getOpener(head):
        # 处理cookies
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(pro)
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener
    @staticmethod
    def queryPlayer():
        url = "http://www.volleychina.org/team/w/"
        opener = getPlayerDate.getOpener(getPlayerDate.header)
        op = opener.open(url)
        data=op.read()
        data=PyQuery(data)
        #读取球队的id号以及球队名字
        team=list()
        teamNum=data(".teamblock").length
        for i in range(teamNum):
            team.append(
                {
                #读取id号
                "id":data(".teamblock:nth-child("+str(i+1)+")").attr("id"),
                #读取球队名
                "name":data(".teamblock:nth-child("+str(i+1)+")").text()
            }
            )
            #存入数据库中
            database.clubDb.creatTeam(team[i])

        #依次读取各个球队的队员信息
        for index in(range(len(team))):
            #将位置转换为中文
            def positionToZH(num):
                if num==1:
                    return "主攻"
                if num==2:
                    return "副攻"
                if num==3:
                    return "接应"
                if num==4:
                    return "二传"
                if num==5:
                    return "自由人"

            #将取得的id号拼接为一个url
            url="http://cva.sports.sina.com.cn/api/player/getByTeamId?teamId="+str(team[index]["id"])+"&callback=drawit2&dpc=1"

            op=opener.open(url)
            data = op.read()
            data=data.decode("gbk")
            num=str.find(data,"data")
            #将字符串切分，方便处理为dict
            data=data[num+7:-17]
            data=str.split(data,"},")
            res=list()
            for index in range(len(data)-1):
                data[index]+="}"
                #转换为dict
                playerDict=eval(data[index])
                #将位置号转化为中文
                playerDict["position"]=positionToZH(int(playerDict["position"]))
                res.append(playerDict)
                database.playerDb.creatPlayer(playerDict)

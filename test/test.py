# -*- coding:utf-8 -*-
from src.thread import getPlayerDataThread

if __name__ == "__main__":
    queryThread = getPlayerDataThread()

    queryThread.start()

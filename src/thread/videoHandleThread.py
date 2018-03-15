#将视频处理之后发回界面线程处理
# -*- coding:utf-8 -*-

import numpy
import cv2
from src.worker.edgeDetect import edgeDetect
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
class videoHandleThread(QtCore.QThread):

    #发送处理完的一帧回界面(当前画面以及当前时间)
    sendFrameSignal = QtCore.pyqtSignal(QPixmap,str)
    #当前帧的index
    currentFrameIndexSignal = QtCore.pyqtSignal(int)
    #发送视频信息回界面线程(总帧数以及时间以及码率)
    senVideoProp =  QtCore.pyqtSignal(int,str)

    def __init__(self,filename,framSize,parent=None):
        super(videoHandleThread, self).__init__(parent)
        #帧大小
        self.filename=filename
        self.framSize=framSize
        self.goOn=True
        self.haveGetQuitSignal=False
        self.cap=cv2.VideoCapture(self.filename)
        self.framToChange=-1

    def run(self):
        #总帧数
        framCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps=self.cap.get(cv2.CAP_PROP_FPS)
        videoTotalTime = self.mescToStr(framCount/fps)
        self.senVideoProp.emit(framCount,videoTotalTime)
        index = 0
        while (self.cap.isOpened()and not self.haveGetQuitSignal):
            if self.goOn:
                #是否收到改变当前帧的信号
                if self.framToChange != -1:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.framToChange)
                    self.framToChange=-1
                ret, frame = self.cap.read()
                cv2.imwrite("trainingFrame" + str(index) + ".jpg", frame)
                index += 1

                currentFrameIndex=int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                #注意：显示的时间不是正常播放的时间
                currentTime=self.mescToStr(currentFrameIndex/fps)
                frame=edgeDetect.cannyDetect(frame)
                #转换为QPixmap
                frameImage=Image.fromarray(frame)
                frameImage=frameImage.resize((self.framSize.width(),self.framSize.height()))
                framePixmap = QPixmap.fromImage(ImageQt(frameImage))

                #改变当前帧的大小适应窗口
                framePixmap.scaled(self.framSize)
                #将当前帧、帧的index、当前帧所处时间 发回界面线程
                self.sendFrameSignal.emit(framePixmap,currentTime)
                self.currentFrameIndexSignal.emit(currentFrameIndex)


                if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                    break

            #暂停，100毫秒之后再检查是否收到继续信号
            else:
                self.msleep(100)
        self.cap.release()

    #主界面大小改变
    def onReceiveVideoLabelResize(self,size):
        self.framSize=size

    def onReceivePauseSignal(self):
        self.goOn=not self.goOn

    def onReceiveQuitSignal(self):
        self.haveGetQuitSignal=True

    #收到当前帧改变的信号
    def onReceiveCurrentFrameChangeSignal(self,frameToChange):
        self.framToChange=frameToChange
    #将毫秒数转化为 00:00时间显示
    def mescToStr(self,timestamp):
        m, s = divmod(timestamp, 60)
        h, m = divmod(m, 60)
        return ("%02d:%02d:%02d" % (h, m, s))


# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QListWidgetItem
from src.thread import videoHandleThread
from src.thread.getPlayerDataThread import getPlayerDataThread
from src.ui import ui_MainWindow
from src.ui import framlessWindow
from PyQt5.QtWidgets import QMessageBox
from resource.resource import *
from PyQt5.QtCore import  QPoint

class mainWindow(QtWidgets.QMainWindow,framlessWindow.QUnFrameWindow, ui_MainWindow.Ui_MainWindow):

    resizeSignal = QtCore.pyqtSignal(QtCore.QSize)
    #标识线程是否继续工作信号(处理暂停操作)
    goOnSignal = QtCore.pyqtSignal(bool)
    #通知工作线程停止处理视频信号
    quitSignal = QtCore.pyqtSignal()
    #改变当前帧
    currentFrameChangeSignal = QtCore.pyqtSignal(int)

    def __init__(self,**kwds):
        super().__init__(**kwds)

        self.setupUi(self)
        #self.__center__()
        self.retranslateUi(self)
        #加载图片
        self.__initIcon()
        self.__initConnect__()
        self.filename=None
        #标识线程是否初始化
        self.workThreadHasStart=False
        #标识工作线程是否正在运行
        self.isWorking = False

        #实现无边框窗体
        self._padding = 5  # 设置边界宽度为5
        self.initLayout() # 设置框架布局
        self.initTitleLabel()  # 安放标题栏标签
        self.setWindowTitle = self._setTitleText(self.setWindowTitle) # 用装饰器将设置WindowTitle名字函数共享到标题栏标签上
        self.setWindowTitle("mitontte")
        self.setMouseTracking(True) # 设置widget鼠标跟踪
        self.initDrag() # 设置鼠标跟踪判断默认值
        self.loadQSS()

     #加载qss
    def loadQSS(self):

        file = QtCore.QFile(':/qss/mainwindow.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        #styleSheet是QByteArray，先转为bytes 再转为str
        self.setStyleSheet(styleSheet.data().decode("utf-8"))

    def __center__(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #初始化信号槽
    def __initConnect__(self):
        self.actionOpenFile.triggered.connect(self.openFile)
        self.btn_start.clicked.connect(self.onBtnStart)
        self.horizontalSlider_progress.sliderReleased.connect(self.onVideoSliderRealeaesd)
        self.actionSpider.triggered.connect(self.onActionSpiderTriggered)

    #初始化图标
    def __initIcon(self):

        volumeImg=QPixmap(":/img/speaker.png")
        self.btn_start.setIcon(QIcon(":/img/play-button.png"))
        self.label_volume.setPixmap(volumeImg)

    #打开文件

    def openFile(self):

        #重新初始化标识
        #标识线程是否初始化
        self.workThreadHasStart=False
        #标识工作线程是否正在运行
        self.isWorking = False
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if filename:
            # 发送关闭之前进程的信号
            self.quitSignal.emit()
            self.filename=filename
            item=QListWidgetItem()
            item.setText(filename.split("/")[-1]+"  加载成功")
            self.listWidget_comment.addItem(item)

    #开始处理并播放视频
    def onBtnStart(self):
        #要选择了输入文件后才进行处理
        if self.filename:
            #初次开始线程
            if  not self.workThreadHasStart:
                self.workThreadHasStart=True
                self.isWorking=True
                self.btn_start.setIcon(QIcon(":/img/pause.png"))
                self.videoHandleThread=videoHandleThread(self.filename,self.label_video.size())

                #connect
                self.videoHandleThread.sendFrameSignal.connect(self.onReceiveFram)
                self.videoHandleThread.currentFrameIndexSignal.connect(self.onReceiveCurrentFrameIndex)
                self.resizeSignal.connect(self.videoHandleThread.onReceiveVideoLabelResize)
                self.goOnSignal.connect(self.videoHandleThread.onReceivePauseSignal)
                self.videoHandleThread.senVideoProp.connect(self.onGetFrameCount)
                self.quitSignal.connect(self.videoHandleThread.onReceiveQuitSignal)
                self.currentFrameChangeSignal.connect(self.videoHandleThread.onReceiveCurrentFrameChangeSignal)
                #滑动进度条时不再接收当前帧的信号
                self.horizontalSlider_progress.sliderPressed.connect(self.onSliderPressed)
                #启动处理线程

                self.videoHandleThread.start()
            else:
                #线程正在工作，发送暂停信号
                if self.isWorking:
                    self.isWorking=False
                    self.goOnSignal.emit(False)
                    self.btn_start.setIcon(QIcon(":/img/play-button.png"))
                #线程未工作，发送继续信号
                else:
                    self.isWorking=True
                    self.goOnSignal.emit(True)
                    self.btn_start.setIcon(QIcon(":/img/pause.png"))
    def onSliderPressed(self):
        if self.workThreadHasStart:
            self.videoHandleThread.currentFrameIndexSignal.disconnect(self.onReceiveCurrentFrameIndex)

    #根据当前帧数改变slider
    def onReceiveCurrentFrameIndex(self,currentFrameIndex):
        self.horizontalSlider_progress.setValue(currentFrameIndex)

    #接收被处理的视频帧 并显示
    def onReceiveFram(self,frame,currentTime):
        self.label_rest_time.setText(currentTime+"/"+self.videoTotalTime)
        self.label_video.setPixmap(frame)

    #得到总帧数
    def onGetFrameCount(self,framCount,videoTotalTime):

        #单位是毫秒
        self.videoTotalTime=videoTotalTime
        self.horizontalSlider_progress.setMaximum(framCount)

    def onVideoSliderRealeaesd(self):
        if self.workThreadHasStart:
            self.videoHandleThread.currentFrameIndexSignal.connect(self.onReceiveCurrentFrameIndex)
            self.currentFrameChangeSignal.emit(self.horizontalSlider_progress.value())

    #爬取球员数据
    def onActionSpiderTriggered(self):
        #新建爬取球员数据线程
        self.queryThread=getPlayerDataThread()
        self.queryThread.finishSignal.connect(self.finishSpider)
        self.queryThread.start()
        QMessageBox.information(self, "wait", "爬虫开始工作，请耐心等待\n大约需要10秒")

    #爬虫线程工作结束
    def finishSpider(self,finishTag):
        if finishTag==0:
            QMessageBox.information(self,"error", "网络错误")
        if finishTag==1:
            QMessageBox.information(self,"ok", "爬虫工作完成")

    #变更后的视频播放label的size发给工作线程
    def resizeEvent(self, *args, **kwargs):
        # 自定义窗口调整大小事件
        self._TitleLabel.setFixedWidth(self.width()) # 将标题标签始终设为窗口宽度
        # 分别移动三个按钮到正确的位置
        try:
            self._CloseButton.move(self.width() - self._CloseButton.width(), 0)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 3 + 1, 0)
        except:
            pass
        try:
            self._MaximumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 + 1, 0)
        except:
            pass
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                           for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                         for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                    for y in range(self.height() - self._padding, self.height() + 1)]

        self.resizeSignal.emit(self.label_video.size())

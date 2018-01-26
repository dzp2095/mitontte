# -*- coding:utf-8 -*-
#边沿检测
import numpy
import cv2

class edgeDetect:
    def __init__(self):
        return
    @staticmethod

    #canny算法
    def cannyDetect(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(gray, (3, 3), 0)
        canny = cv2.Canny(frame, 50, 150)
        return canny

    #Laplacian算法
    @staticmethod
    def laplacianDetect(frame):
        cap = cv2.VideoCapture('test.avi')
        index = 0
        while (cap.isOpened()):
            index += 1
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            lap = cv2.Laplacian(gray, cv2.CV_64F)
            cv2.imshow("Edge detection by Laplacaian", numpy.hstack([lap, gray]))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    #sobel算法
    @staticmethod
    def sobelDetect(frame):

        cap = cv2.VideoCapture('test.avi')
        index = 0
        while (cap.isOpened()):
            index += 1
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
            sobelx = numpy.uint8(numpy.absolute(sobelx))
            sobely = numpy.uint8(numpy.absolute(sobely))
            sobelcombine = cv2.bitwise_or(sobelx, sobely)


            cv2.imshow("Edge detection by Sobel", numpy.hstack([ gray,sobelx, sobely, sobelcombine]))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()




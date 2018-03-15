# -*- coding:utf-8 -*-
from src.thread import getPlayerDataThread
import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    cap = cv2.VideoCapture("C:/Users/dengzhipeng/Documents/GitHub/mitontte/resource/video/第1轮-上海女排31北京女排-全场.MP4")
    index = 0
    while (cap.isOpened()):
        index += 1
        ret, frame = cap.read()
        img=frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(gray, (3, 3), 0)
        canny = cv2.Canny(frame, 50, 150)
        lines = cv2.HoughLines(canny, 1, np.pi / 180, 500)
        cv2.imwrite("训练帧" + str(index) + ".jpg", frame)
        index += 1
        if lines is not None:
            for index in range(len(lines)):
                for rho, theta in lines[index]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    print(a, b)
                    x0 = a * rho
                    y0 = b * rho

                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow('Canny', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


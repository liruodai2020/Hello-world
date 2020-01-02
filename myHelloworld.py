# coding=utf-8

import numpy as np
import cv2
import matplotlib.pyplot as plt


def cropSameSize(img1, img2):
    height, width = img2.shape[:2]
    img1 = img1[:height, :width, :]
    return img1


def demoMergeAppleAndOrange():
    octaveLevel = 5
    appleImg = cv2.imread('apple2.jpg')
    orangeImg = cv2.imread('orange.png')
    imgHeight, imgWidth = appleImg.shape[:2]
    halfApple = appleImg[:, :imgWidth//2, :]
    halfOrange = orangeImg[:, imgWidth//2:, :]

    tempGpy = halfApple.copy()
    gpyApple = [tempGpy]
    for i in range(octaveLevel):
        tempGpy = cv2.pyrDown(tempGpy)
        gpyApple.append(tempGpy)

    tempGpy = halfOrange.copy()
    gpyOrange = [tempGpy]
    for i in range(octaveLevel):
        tempGpy = cv2.pyrDown(tempGpy)
        gpyOrange.append(tempGpy)

    lpyApple = [gpyApple[-1]]
    for i in range(octaveLevel, 0, -1):
        tempLpy = cv2.subtract(gpyApple[i-1], cropSameSize(cv2.pyrUp(gpyApple[i]), gpyApple[i-1]))
        lpyApple.append(tempLpy)

    lpyOrange = [gpyOrange[-1]]
    for i in range(octaveLevel, 0, -1):
        tempLpy = cv2.subtract(gpyOrange[i-1], cropSameSize(cv2.pyrUp(gpyOrange[i]), gpyApple[i-1]))
        lpyOrange.append(tempLpy)

    lpyMerged = [np.hstack((img1, img2)) for img1, img2 in zip(lpyApple, lpyOrange)]
    temp = lpyMerged[0].copy()
    for i in range(1, octaveLevel+1):
        temp = cv2.add(lpyMerged[i], cropSameSize(cv2.pyrUp(temp), lpyMerged[i]))
    mergedImg = temp
    cv2.imshow('5', mergedImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('AppleOrange.png', mergedImg)

if "__main__" == __name__:
    img = cv2.imread('apple2.jpg')
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, binaryImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(contours[0])
    cv2.drawContours(binaryImg, contours, -1, (0, 0, 255), 2)
    plt.imshow(img)
    plt.imshow(binaryImg)
    plt.show()

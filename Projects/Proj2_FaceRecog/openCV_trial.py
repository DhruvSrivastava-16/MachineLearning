# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:23:58 2020

@author: DHRUV
"""

import cv2
img = cv2.imread('intel.jpg')
gray = cv2.imread('intel.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',img)
cv2.imshow('gray',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
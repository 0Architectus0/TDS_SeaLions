#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 17:31:04 2017

@author: benharris
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.color import rgb2gray,rgba2rgb
from scipy.ndimage import gaussian_filter
from skimage.filters import gaussian,sobel
from skimage import data
from skimage import img_as_float
from skimage.morphology import reconstruction
from skimage import feature
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from skimage import color
from webcolors import rgb_to_name
from skimage import novice

def getSquare(contour):
    x = min(contour[:, 1])-20
    y = min(contour[:, 0])-20
    w = (max(contour[:, 1])-min(contour[:, 1]))+20
    h = (max(contour[:, 0])-min(contour[:, 0]))+20
    return x,y,h,w

def getCenter(contour):
    x = np.median(contour[:, 1])
    y = np.median(contour[:, 0])
    return (x,y)

def getGreen(img):
    if (img[0]<60 and img[1]>160 and img[2]<50):
        return True
    else:
        return False
    
def getColor(img):
    if (img[0]>175 and img[1]<20 and img[2]<30):
        return True,'Red'
    elif (img[0]<40 and img[1]<70 and img[2]>150):
        return True,'Blue'
    elif (img[0]>70 and img[0]<100 and img[1]<60 and img[1]>30 and img[2]<20):
        return True,'Brown'
    elif (img[0]<40 and img[1]>175 and img[2]<30):
        return True,'Green'    
    elif (img[0]>220 and img[1]<50 and img[2]>220):
        return True,'Pink'
    else:
        return False,'Unknown'

def replaceColor(img):
    x = img.shape[1]   
    y = img.shape[0]
    for w in range(0, x):
        for h in range(0, y):
            truth = getGreen(img[h,w])
            if (truth):
                img[h,w] = [0,255,0]
    return img
    
# Convert to float: Important for subtraction later which won't work with uint8
orig = io.imread('/Users/benharris/Documents/Projects/SeaLions/images/test4.jpg')
orig = replaceColor(orig)
gray = rgb2gray(orig)
#image = io.imread('/Users/benharris/Documents/Projects/SeaLions/images/4.jpg',flatten=True)
#image = gaussian_filter(image, 1)


edges3 = feature.canny(gray, sigma=1,low_threshold=.01,high_threshold=.15)
#edges3 = roberts(image)
io.imshow(edges3)
io.show()


contours = find_contours(edges3, .8, fully_connected='high', positive_orientation='low')
fig, ax = plt.subplots()
ax.imshow(orig)

for n, contour in enumerate(contours):
    x,y,w,h = getSquare(contour)
    x_c,y_c = getCenter(contour)
    boolean,color = getColor(orig[y_c,x_c])
    #ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    if(boolean):
        print(x,y,w,h)
        print(orig[y_c,x_c][0])
        circ = plt.Circle((x_c, y_c), radius=.1, color='b')
        ax.add_patch(circ)
        ax.add_patch(
        patches.Rectangle(
            (x, y),
            h+20,
            w+20,
            fill=False      # remove background
        ))

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
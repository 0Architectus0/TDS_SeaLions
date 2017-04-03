#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 17:31:04 2017

@author: benharris
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
from skimage.filters import gaussian,sobel
from skimage import data
from skimage import img_as_float
from skimage.morphology import reconstruction
from skimage import feature
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from skimage import color

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

# Convert to float: Important for subtraction later which won't work with uint8
orig = io.imread('/Users/benharris/Documents/Projects/SeaLions/images/test2.png')
image = io.imread('/Users/benharris/Documents/Projects/SeaLions/images/test2.png', flatten=True)
#image = gaussian_filter(image, 1)


seed = np.copy(image)
seed[1:-1, 1:-1] = image.min()
mask = image

dilated = reconstruction(seed, mask, method='dilation')

hdome = image - dilated


edges3 = feature.canny(hdome, sigma=1,low_threshold=.01,high_threshold=.15)
io.imshow(edges3)
io.show()


contours = find_contours(edges3, .8, fully_connected='high', positive_orientation='low')
fig, ax = plt.subplots()
ax.imshow(orig)

for n, contour in enumerate(contours):
    x,y,w,h = getSquare(contour)
    x_c,y_c = getCenter(contour)
    #ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    if (orig[y_c,x_c][0]>190):
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
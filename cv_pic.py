#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy


# In[2]:


class cv_pic():

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

    def pic_in(in_path, out_path):
        target = cv.imread(in_path)
        target.tofile(out_path)
        return target.shape, target

    def pic_out(in_path, win, shape):
        data_out = numpy.fromfile(in_path, dtype = numpy.uint8)
        final = data_out.reshape(shape[0], shape[1], shape[2])
        cv.namedWindow(win, cv.WINDOW_NORMAL)
        cv.imshow(win, final)
        cv.waitKey(0)


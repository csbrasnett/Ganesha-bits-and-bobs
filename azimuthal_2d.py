#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:16:42 2020

@author: Chris
"""

import matplotlib.pyplot as plt
import numpy as np

#load in the azimuthal data
f = 'file here'

d = np.genfromtxt(f, delimiter = ',')

#get the data from the columns
x = d[0:,0]
y = d[0:,1]
z = np.nan_to_num(d[0:,2])

z_2d = z.reshape(len(np.unique(x)), len(np.unique(y))).T

#make the figure. Need to adjust the aspect and clim to make sure it looks ok.
fig, ax = plt.subplots(1,1, figsize = (10,10))
ax.imshow(z_2d, extent = (min(x), max(x), min(y), max(y)), aspect = 0.001, clim = (0,500))
ax.set_xlabel('q (Å$^{-1}$)')
ax.set_ylabel('Angle')

#opttino for cutting off the x axis at a more sensible q value
ax.set_xlim(0,0.3)


q_lo = 0.09
q_hi = 0.1

#find where q is within a certain range
get_range_indices = np.where((x<q_hi)&(x>q_lo))

#get the y and z values for this range of q
y_cut = y[get_range_indices]
z_cut = z[get_range_indices]

#y is then multiple ranges of 0-360 degrees that need to have the z values averaged over
y_cut_final = np.zeros(0)
z_cut_averaged = np.zeros(0)

#for every unique value in the y_cut...
for i in range(len(np.unique(y_cut))):
    #find the indicies of the unique value
    find = np.where(y_cut==np.unique(y_cut[i]))
    
    #note the value of y here
    y_cut_final = np.append(y_cut_final, y_cut[find][0])
    
    #the find the average of the corresponding z indicies and append it to the final array
    z_cut_averaged = np.append(z_cut_averaged, z_cut[find].mean())
    
    
#now do a line plot of the intensity in this region
fig1, ax1 = plt.subplots(1,1,figsize=(5,5))
ax1.plot(y_cut_final, z_cut_averaged)
ax1.set_xlabel('Angle')
ax1.set_ylabel('Intensity (Arbitrary Units)')
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 13:34:22 2016

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
'''

begin editable section

IMPORTANT! ENSURE ALL SIG FIGS ARE BEING EXPORTED FROM TRIPLET EXPORT IN SAXSGUI!!!!

'''

#the path to the txt file
file_path='your/path/here'

#the maximum colour limit for the figure
colour_max=10

#boolean for saving the figure
save_fig=False

#folder to where the image should be saved
save_path='your/path/here'

#the name of the image
save_name='7106'

#the extension with which to save the image
save_extension='.png'

#dpi quality of the image
save_quality=200

'''
end editable section
'''


table=np.genfromtxt(file_path,dtype='float',delimiter=',', filling_values=0, unpack=True)

x_s=np.genfromtxt(file_path,dtype='float',delimiter=',',usecols=0, filling_values=0, unpack=True)
y=np.genfromtxt(file_path,dtype='float',delimiter=',',usecols=1, filling_values=0, unpack=True)
z_init=np.genfromtxt(file_path,dtype='float',delimiter=',',usecols=2, filling_values=0, unpack=True)

z=np.nan_to_num(z_init)

z=z.reshape(np.size(np.unique(x_s)),np.size(np.unique(y))).T
z=np.flipud(z)

fig,ax = plt.subplots()


ax.imshow(z, extent=(np.amin(x_s),np.amax(x_s),np.amin(y),np.amax(y)),cmap=cm.viridis,clim=(0,colour_max))
ax.set_xlabel('x, A$^{-1}$')
ax.set_ylabel('y, A$^{-1}$')

t=save_path+save_name+save_extension

fig.tight_layout()

if save_fig==True:
    fig.savefig(t,dpi=200,frameon=False,bbox_inches='tight')

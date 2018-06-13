# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

import matplotlib.pyplot as plt
import numpy as np
import glob

'''
begin editable section

This code is for showing a series of scattering patterns from the same series, offset by a certain spacing.

Corrections made to ensure no overlapping between patterns
'''


#folder containing csvs of I vs q data
data_folder='your/path/here'

#list of log numbers of the run that you're interested in plotting
these_files=[]

#list of sample names (in log book order) to go in the legend
labels=[]

#the lower and upper limits in q for the data that you want to plot
lower_limit=0.03
upper_limit=0.2

#sort out the legend
#the number of columns for the legend
no_legend_columns=4

#the x and y position of the legend beneath the plot, and the
legend_x_position=0.9
legend_y_position=-0.15

#bool variable for having a frame around the plot
frame_variable=False

#bool for saving the figure that you make. Set True for saving, False if not
save_fig=False

#folder path in which to save the figure
save_fig_in='your/path/here'

#a name for the figure
fig_name='your figure name'

#the extension for the figure: png for short use, tiff for publication
fig_extension='.png'

#dpi quality for the saved figure
fig_quality=200

'''
end editable section
'''

files=glob.glob(data_folder+'*.csv')

matches=[]
for i in these_files:
    match=[s for s in files if i in s]
    matches.append(match[0])

last_y=0
for j in range(len(matches)):
    table=np.genfromtxt(matches[j],skip_header=10,delimiter=',')
    
    x_data=table[np.intersect1d(np.where(table[0:,0]>lower_limit),np.where(table[0:,0]<upper_limit)),0]
    y_data=table[np.intersect1d(np.where(table[0:,0]>lower_limit),np.where(table[0:,0]<upper_limit)),1]
    
    norm=(y_data/np.max(y_data))*10*(j+1)

    if j==0:
        plt.plot(x_data,norm,label=labels[j])
        last_y=max(norm)
    
    elif j>0:
        this_min=np.min(norm)
        
        if last_y>this_min:
            norm_new=norm+(last_y-this_min)+5
            plt.plot(x_data,norm_new,label=labels[j])
            last_y=max(norm_new)
            
        else:
            plt.plot(x_data,norm,label=labels[j])
            last_y=max(norm)

lgd=plt.legend(ncol=no_legend_columns,bbox_to_anchor=(legend_x_position,legend_y_position), frameon=frame_variable)
plt.xlabel('$q$ (Å$^{-1}$)')
plt.ylabel('Intensity (A.U.)')
plt.tight_layout()
if save_fig==True:
    plt.savefig(save_fig_in+fig_name+fig_extension,dpi=fig_quality, bbox_extra_artists=(lgd,), bbox_inches='tight')    
plt.show()
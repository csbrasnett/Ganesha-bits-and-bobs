# -*- coding: utf-8 -*-
"""

author: Chris Brasnett, University of Bristol, christopher.brasnett@bristol.ac.uk

"""

'''
start of editable section

in_dir - directory where the csv files from Ganesha are stored. Assumes a structure of ~/this_experiment/csv/
         dat files will then be saved in the folder (automatically created by this programme) ~/this_experiment/dat/
         The naming assumes that the files have come from Ganesha.
         
empty - the log book code for the empty capillary
buffer - the log book code for the buffer for the experiment.
'''
in_dir='your/path/here/'

empty= log_book_number_1
buffer= log_book_number_2

'''
end of editable section
'''

import pandas as pd
import numpy as np
import glob
import os

#get all the files from the csv directory
files=glob.glob(in_dir+'*.csv')

#find which are the empty and buffer files
empty_file=[s for s in files if str(empty) in s][0]
buffer_file=[s for s in files if str(buffer) in s][0]

#create a save location folder for dat files
save_location=in_dir[:-4]+'dat/'

#create the folder if it hasn't already been created
try:    
    dir_path_new = os.makedirs(save_location)
except FileExistsError:
    pass

#open the empty and buffer data
empty_data=empty_file
empty_array=pd.read_table(empty_data,skiprows=1,delimiter=',').values

buffer_data=buffer_file
buffer_array=pd.read_table(buffer_data,skiprows=1,delimiter=',').values

#subtract the empty from the buffer. q is the same, I is subtracted, dI=sqrt(sum of errors squared) as standard error
buffer_subtracted=np.zeros(np.shape(buffer_array))
buffer_subtracted[0:,0]=buffer_array[0:,0]
buffer_subtracted[0:,1]=buffer_array[0:,1]-empty_array[0:,1]
buffer_subtracted[0:,2]=np.sqrt((buffer_array[0:,2]**2)+(empty_array[0:,2]**2))

#find which are the remaining actual sample files. Probably a better way to do this...
files1=[]
for i in files:
    test=i.find(str(empty))
    if test==-1:
        files1.append(i)   
sample_files=[]
for i in files1:
    test1=i.find(str(buffer))
    if test1==-1:
        sample_files.append(i)

#for each sample file, subtract the empty capillary, and then subtract the empty-corrected buffer data.
for i in sample_files:
    data=pd.read_table(i,skiprows=1,delimiter=',').values
    
    #subtract the empty off the sample
    sample_subtraction_1=np.zeros(np.shape(data))
    sample_subtraction_1[0:,0]=data[0:,0]
    sample_subtraction_1[0:,1]=data[0:,1]-empty_array[0:,1]
    sample_subtraction_1[0:,2]=np.sqrt((data[0:,2]**2)+(empty_array[0:,2]**2))
    
    #subtract the corrected buffer off the corrected sample
    sample_subtraction_2=np.zeros(np.shape(sample_subtraction_1))
    sample_subtraction_2[0:,0]=sample_subtraction_1[0:,0]
    sample_subtraction_2[0:,1]=sample_subtraction_1[0:,1]-buffer_subtracted[0:,1]
    sample_subtraction_2[0:,2]=np.sqrt((sample_subtraction_1[0:,2]**2)+(buffer_subtracted[0:,2]**2))
    
    #format subtracted sample as pandas dataframe for easy output. NB: naming assumes from Ganesha.
    op_df=pd.DataFrame(sample_subtraction_2)
    op_place=save_location+i[-9:-4]+'.dat'
    
    #save the file
    op_df.to_csv(op_place,sep='\t',index=False,header=False)
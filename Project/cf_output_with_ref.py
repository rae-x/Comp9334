#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Project sample file 

This file compares the output files against their reference.

For trace mode, it checks mrt_*.txt, s1_dep_*.txt, s1_dep_*.txt and 
s3_dep_*.txt

For random mode, it checks mrt_*.txt only 

This file assume the output files and their reference files
are in the same directory

This version: 6 April 2021 

@author: ctchou
"""

# import sys for input argument 
import sys
import os 

# import numpy for easy comparison 
import numpy as np

def main():
    
    # Check whether there is an input argument 
    if len(sys.argv) == 2:
        t = int(sys.argv[1])
    else:
        print('Error: Expect the test number as the input argument')
        print('Example usage: python3 cf_output_with_ref.py 1')   
        return
    
    # Location of the folders
    out_folder = 'output'
    ref_folder = 'ref'
        
    # Definitions
    file_ext = '.txt' # File extension
    
    # For trace mode, an absolute tolerance is used
    ABS_TOL = 1e-3  # Absolute tolerance 
    
    # For tests 5 and 6 (which is in radnom mode), the mean response time is expected
    # to be within the range 
    MRT_TOL = [[0.2726, 0.3110],[0.4678, 0.5610]]
    
    # Read test number from the input argument 
       
    # t is the test number
    # Tests 1, 2 and 3 are trace mode
    # Test 4 is radnom mode
    if t in {1,2,3}: 
    
        # Compare mrt against the reference
        out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
        ref_file = os.path.join(ref_folder,'mrt_'+str(t)+'_ref'+file_ext)
        
        if os.path.isfile(out_file):
            mrt_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return
        
        if os.path.isfile(ref_file): 
            mrt_ref = np.loadtxt(ref_file)
        else:
            print('Error: File ',ref_file,'does NOT exist')    
            return           
        
        if np.isclose(mrt_stu,mrt_ref,atol=ABS_TOL):
            print('Test '+str(t)+': Mean response time matches the reference')
        else: 
            print('Test '+str(t)+': Mean response time does NOT match the reference')
    
        # Compare s1_dep, s2_dep, s3_dep against the reference
        for k in range(1,4):   
            out_file = os.path.join(out_folder,'s'+str(k)+'_dep_'+str(t)+file_ext)
            ref_file = os.path.join(ref_folder,'s'+str(k)+'_dep_'+str(t)+'_ref'+file_ext)
            
            if os.path.isfile(out_file):
                dep_stu = np.loadtxt(out_file)
            else:
                print('Error: File ',out_file,'does NOT exist')    
                return            
            
            if os.path.isfile(ref_file):
                dep_ref = np.loadtxt(ref_file)
            else:
                print('Error: File ',ref_file,'does NOT exist')    
                return      
            
            if np.all(np.isclose(dep_stu,dep_ref,atol=ABS_TOL)):
                print('Test '+str(t)+': s'+str(k)+' departure times match the reference')
            else: 
                print('Test '+str(t)+': s'+str(k)+' departure times do NOT match the reference')
    
    elif t == 4:  
        print('Test 4 is obsolete. Please use Tests 5 and 6 for random mode.')
    
    
    elif 5 <= t <= 6: 
        out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
       
        if os.path.isfile(out_file):
            mrt_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return        
    
        
        if MRT_TOL[t-5][0] <= mrt_stu <= MRT_TOL[t-5][1]:
            print('Test '+str(t)+': Mean response time is within tolerance')
        else: 
            print('Test '+str(t)+': Mean response time is NOT within tolerance')
            print('You should try to run a new simulation round with new random numbers.')
            print('Your output need to be within the tolerance for most of the rounds.')
        
        
if __name__ == '__main__':
    main()            
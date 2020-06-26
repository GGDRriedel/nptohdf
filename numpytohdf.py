'''provides a function to convert np.arrays into a hdf5 model for gprmax'''


import os
import h5py
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy.signal import find_peaks 

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def np_to_hdf(input_array,dx,dy,dz,filename='out.h5'):
    hdf5file = os.path.splitext(filename)[0] + '.h5'
    zcells=1
    
    #read data
    data=input_array
    data_grey=np.floor(rgb2gray(data))
    n=plt.hist(data_grey.flatten(),bins=range(255))
    peaks,_=find_peaks(np.concatenate(([min(n[0])],n[0],[min(n[0])])), prominence=1000)
    materials=n[1][peaks]
    print("Found {} Materials".format(len(materials)))
    
    
    materials=materials-1
    materials[-1]=materials[-1]+1
    materials
    
    # Array to store geometry data (initisalised as background, i.e. -1)
    arraydata = np.ones((data.shape[0], data.shape[1], zcells), dtype=np.int16) * -1
    dx_dy_dz = (dx,dy,dz)
    
    
    
    # Write geometry (HDF5) file
    with h5py.File(hdf5file, 'w') as fout:
    
        # Add attribute with name 'dx_dy_dz' for spatial resolution
        fout.attrs['dx_dy_dz'] = dx_dy_dz
    
        # Use a boolean mask to match selected pixel values with position in image
        for i, material in enumerate(materials):
            mask = data_grey == material
            arraydata[mask] = i
            np.sum(mask)
            #print(i,material,np.sum(mask))
    
        # Write data to file
        fout.create_dataset('data', data=arraydata)
        print("Wrote Model Data to {}".format(hdf5file))
# -*- coding: utf-8 -*-

# BSD 3-Clause License
#
# Copyright (c) 2020, Lawson Health Research Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Module to import log, data and transducer position files for PAI128 systems


Lawson Optics Lab
Lawson Health Research Institute
Western University
London, ON, Canada

Created by: Lawrence Yip
Last Modified 2021-04-30
"""


import numpy as np
from pathlib import Path #for operating system paths
from numba import prange # for multithreading
import pandas as pd #for loading CSV file
import math




def importPAI128(raw_data_filename):
    """
    read PAI128 raw pv3 files and settings

    Parameters
    ----------
    raw_data_filename : TYPE
        DESCRIPTION. Filename of the pv3 file to load

    Returns
    -------
    UserID : TYPE
        DESCRIPTION. basically unused
    DAQsettings : TYPE
        DESCRIPTION. all the data, metadata and raw data outputted
    tkdata : TYPE
        DESCRIPTION. TrakSTAR data

    """
    def fread(fidint, nelements, dtype): #simulate Matlab fread, and squeeze if single elements read
        if dtype is np.str:
            dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
        else:
            dt = dtype
        data = np.fromfile(fidint, dt, nelements)

        if np.size(data) == 1: #squeeze if not an array
            data = np.squeeze(data)
            if np.size(data) ==1:
                data = np.squeeze(data)
        return data
    
    fid = open(raw_data_filename, mode="rb") # open the file

    version = fread(fid,1,np.int16) # read version metadata (unused)
    UserID = fread(fid,1,np.int16) # read userid metadata (unused)
    DAQsettingssize = fread(fid,1,np.int32) # read DAQsettingssize (i.e. how many DAQ boards are connected)    
    DAQsettings = {}
    
    for ii in range(DAQsettingssize): #note that orders are in Matlab Fortran order, hence the "F" switches
        DAQsettings_perDAQ = {"NumPoints" : fread(fid,1,np.int32),"NumTriggers" : fread(fid,1,np.int32),
                           "NumChannels" : fread(fid,1,np.int32)}
        fread(fid,1,np.int8)
        DAQsettings_perDAQ["TransferRate"] = fread(fid,1,np.double)
        DAQsettings_perDAQ["TimeStamp"] = fread(fid,1,np.int32)
        messagesize = fread(fid,1,np.int32)
        message = fread(fid,messagesize,np.uint8)
        datasize = np.uint32(fread(fid,1,np.uint32)/2)
        DAQsettings_perDAQ["DataPointsCombined"] = fread(fid,datasize,np.uint16)
                    
        for jj in range(DAQsettings_perDAQ.get("NumChannels")):
            reshaped = DAQsettings_perDAQ.get("DataPointsCombined")
            reshaped = reshaped.reshape(np.uint32(datasize/DAQsettings_perDAQ.get("NumChannels")), 
                                        DAQsettings_perDAQ.get("NumChannels"), order="F")
                                  
            reshaped = np.ndarray.byteswap(reshaped[:,:])
            reshaped = np.transpose(reshaped)
            reshaped = np.delete(reshaped,0,1)
            DAQsettings_perDAQ["DataPoints"] = reshaped
            
        DAQsettings[ii] = DAQsettings_perDAQ
        
    #Trakstar function, only used if Trakstar is connected, untested
    tkEnabled = fread(fid,1,np.int8)
    if tkEnabled != 0:
        tkNumSensors = fread(fid,1,np.uint8)
        tkdata = []
        tkdatasizerow = fread(fid,1,np.uint32)
        tkdatasizecolumn = fread(fid,1,np.uint32)
        # tkdata = fread(fid,6,np.double)
        for tk in range(tkdatasizerow):
            tkdata1 = fread(fid,tkdatasizecolumn,'double')
            if np.size(tkdata) == 0:
                tkdata = tkdata1
            else:
                tkdata = np.append([tkdata], [tkdata1], axis=0);
            
    else:
        tkdata = []
        
    fid.close() # close file

    return UserID, DAQsettings, tkdata

def DAQ128settings2RF(DAQ128settings, CheckAveraging):
    # Set array size if averaging will be used
    if (DAQ128settings.get(0, {}).get("NumTriggers")) > 1 and CheckAveraging == True:
        RFdata = np.zeros((len(DAQ128settings)*DAQ128settings.get(0, {}).get("NumChannels"), 
                       DAQ128settings.get(0, {}).get("NumPoints")*256),
                      dtype = np.single, order="F")
    # Set array size if no averaging (or if just turned off)
    else:
        RFdata = np.zeros((len(DAQ128settings)*DAQ128settings.get(0, {}).get("NumChannels"),
                       DAQ128settings.get(0, {}).get("NumPoints")*256*DAQ128settings.get(0, {}).get("NumTriggers")),
                      dtype = np.single, order="F")
        
    # Sort the data. Checking if it should be averaged, and if multiple triggers were used during acquisition
    for ii in DAQ128settings:
        basen = ii * DAQ128settings.get(ii, {}).get("NumChannels")
        
        if  (DAQ128settings.get(ii, {}).get("NumTriggers") > 1 and CheckAveraging == True):
            temp = DAQ128settings.get(ii, {}).get("DataPoints")
            temp = temp.reshape(DAQ128settings.get(ii, {}).get("NumChannels"),-1, 
                                DAQ128settings.get(ii, {}).get("NumTriggers"),order="F")
            temp = np.mean(temp,2)
            
        else:
            temp = DAQ128settings.get(ii, {}).get("DataPoints")
            
        RFdata[(basen):(basen + DAQ128settings.get(ii, {}).get("NumChannels")),:] = temp
        
    return RFdata

def import_and_process_binary(raw_data_folder_path, num_scans, signal_inv=False, left_shift=12,
                 thresholding=0, photodiode=65, Averaging=True, end_remove=80, fluence_correc=False, EffSamp = 1):
    
    #Determine initial values for sample length, number of channels, etc
    _, initial_values, tkdata_initial = importPAI128(Path(raw_data_folder_path, "00000.pv3"))
    
    if Averaging == True and EffSamp <= 1:
        imData = np.zeros((num_scans, np.int32(initial_values.get(0, {}).get("NumPoints")*256), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    elif Averaging == False and EffSamp <= 1:
        imData = np.zeros((num_scans, np.int32(initial_values.get(0, {}).get("NumPoints")*256*initial_values.get(0, {}).get("NumTriggers")), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    elif Averaging == True and EffSamp > 1:
        imData = np.zeros((num_scans, np.int32((initial_values.get(0, {}).get("NumPoints")*256)/EffSamp), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    elif Averaging == False and EffSamp >1:
        imData = np.zeros((num_scans, np.int32((initial_values.get(0, {}).get("NumPoints")*256*initial_values.get(0, {}).get("NumTriggers"))/EffSamp), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    
    #Template to flip the signals since our transducers are all inverted in polarity
    reverseGain = -1 * np.ones((initial_values.get(0, {}).get("NumChannels")*len(initial_values), 1),dtype = np.int, order = "F") 
    reverseGain[photodiode,:] = 1
    
    if np.size(tkdata_initial) != 0:
        tkdataEnable = 1
    else:
        tkdataEnable = 0
        
    if tkdataEnable ==1:
        tkdata = np.zeros((np.shape(tkdata_initial)[0],np.shape(tkdata_initial)[1],num_scans),np.double,order='F')
    
    #Load the signals from the binary file
    # AverageFluence = None
    do_not_fluence_correct = False
    for i in range(num_scans):
        count = str(i)
        S = Path(count.zfill(5)+".pv3")
        _, DAQsettings, tkdata_temp = importPAI128(Path(raw_data_folder_path,S))
        RFdata = DAQ128settings2RF(DAQsettings,Averaging)
        
        #Apply inversion
        if signal_inv == True:
            RFdata = RFdata * reverseGain
            
        #Remove voltage offset using fourier
        RFdata = np.transpose(RFdata)
        for iT in prange(initial_values.get(0, {}).get("NumChannels")*len(initial_values)):
            RFdata_F = np.fft.fft(RFdata[:,iT])
            RFdata_F[0] = 0
            RFdata[:,iT] = np.fft.ifft(RFdata_F)
        
        # Do not allow fluence correction if averaging was used in hardware acquisition but not desired for data reading
        # Otherwise all the acquisitions will be normalized to a single photodiode measurement
        if Averaging == False and initial_values.get(0, {}).get("NumTriggers") != 1:
            do_not_fluence_correct = True
        else:
            #Remove last measurements (spikes)
            RFdata[(-end_remove):-1,:] = 0;    
            RFdata[-1,:] = 0;    
            #remove some at beginning and shift to align with laser Q-sync delay
            RFdata[0:left_shift+20,:] = 0;    
            RFdata = np.roll(RFdata,-left_shift,0)   
        
        if thresholding != 0:
            RFdata[abs(RFdata)<thresholding] = 0
            
        if fluence_correc == True and do_not_fluence_correct == False:
            # Old method for averaging. New method simply divides by PD peak
            # if AverageFluence == None:
            #     AverageFluence = np.max(np.mean(initial_values.get(0, {}).get("DataPoints").get(photodiode)))                
            # ShotPower = np.max(RFdata[0:(initial_values.get(0, {}).get("NumPoints")*256/initial_values.get(0, {}).get("NumTriggers")), photodiode])
            # ShotRatio = AverageFluence/ShotPower
            # RFadjusted = RFdata*ShotRatio
            # RFdata = RFadjusted
            RFdata = RFdata/np.max(RFdata[:, photodiode])

        if EffSamp > 1:
            RFdata_temp = np.zeros((np.int32(RFdata.shape[0]/EffSamp), RFdata.shape[1]))
            for j in range (RFdata.shape[1]):
                RFdata_single = RFdata[:,j]
                RFdata_single = np.array(list([sum(RFdata_single[i:i+EffSamp])//EffSamp for i in range(0,len(RFdata_single),EffSamp)]))
                # pa_data_temp[k,:,j] = pa_data_single
                RFdata_temp[:,j] = RFdata_single
                
            RFdata = RFdata_temp
            
        imData[i,:,:] = RFdata
        if tkdataEnable ==1:
            tkdata[:,:,i] = tkdata_temp
    
    if tkdataEnable ==1:
        return imData, tkdata
    else:
        return imData

def load_scan_log(scan_log_file_path, homePath, numIllum = 0, R = 179.25, Method = "trans"):
    """
    

    Parameters
    ----------
    scan_log_file_path : CSV file
    
    Returns
    -------
    transPositionsAllScans : np.array
        Array with all scan positions*transducer positions* XYZ+CoR_XYZ.
    time_taken : Time elapsed to acquire scan
        Time in seconds.

    """
    scan_positions = pd.read_csv(scan_log_file_path) # Load log file
    # R = 254.2772 # Set length of arm between end effector and CoR for 360array
    import datetime
    time_taken = sum(scan_positions["time taken"[:]])
    time_taken = str(datetime.timedelta(seconds=time_taken))
        
    
    # Calculate CoR using scan positions, then append only needed values
    x = pd.Series.to_numpy(scan_positions["x"[:]] - R*np.sin(np.radians(scan_positions["v"[:]]))*np.cos(np.radians(scan_positions["u"[:]])))
    y = pd.Series.to_numpy(scan_positions["y"[:]] - R*np.sin(np.radians(scan_positions["v"[:]]))*np.sin(np.radians(scan_positions["u"[:]])))
    z = pd.Series.to_numpy(scan_positions["z"[:]] - R*np.cos(np.radians(scan_positions["v"[:]])))
    scan_positions_abbrev = np.column_stack((pd.Series.to_numpy(scan_positions["x"[:]]), pd.Series.to_numpy(scan_positions["y"[:]]),
                                             pd.Series.to_numpy(scan_positions["z"[:]]), pd.Series.to_numpy(scan_positions["u"[:]]),
                                             pd.Series.to_numpy(scan_positions["v"[:]]), x, y, z))
    numScans = len(scan_positions_abbrev)
    if Method == "trans":
        try:
            import tables
            file = tables.open_file(homePath)
            transducer_pos_home = file.root.transducer_pos_home[:]
        except:
            import scipy.io as sio
            homepos = sio.loadmat(homePath)
            transducer_pos_home = homepos.get("transducer_pos_home")
        numDet = len(transducer_pos_home)
    elif Method == "Rascevska":
        numDet = 8
        
    
    transPositionsAllScans = np.zeros((numDet,3,numScans))
    if numIllum != 0:
        illumPositionsAllScans = np.zeros((numIllum,3,numScans))
    for i in range(numScans):
        transPositionsAllScans[:,:,i] = TransducerRotTrans(scan_positions_abbrev[i,0], scan_positions_abbrev[i,1], scan_positions_abbrev[i,2],
                                                           scan_positions_abbrev[i,3], scan_positions_abbrev[i,4], R, homePath, Method)
        if numIllum != 0:
            illumPositionsAllScans[:, :, i] = TransducerRotTrans(scan_positions_abbrev[i,0], scan_positions_abbrev[i,1], scan_positions_abbrev[i,2],
                                                           scan_positions_abbrev[i,3], scan_positions_abbrev[i,4], R, homePath, Method ="illum")
    core_array = np.zeros((numDet,3,len(scan_positions_abbrev)))
    for j in range(len(scan_positions_abbrev)):
        cor_array_temp = np.reshape(np.tile(scan_positions_abbrev[j, 5:8],numDet),[3,-1],order="F")
        core_array[:,:,j] = cor_array_temp.T
    transPositionsAllScans = np.append(transPositionsAllScans, core_array,axis=1)
        
    if numIllum != 0:
        core_array_illum = np.zeros((numIllum,3,len(scan_positions_abbrev)))
        for j in range(len(scan_positions_abbrev)):
            cor_array_temp = np.reshape(np.tile(scan_positions_abbrev[j, 5:8],numIllum),[3,-1],order="F")
            core_array_illum[:,:,j] = cor_array_temp.T
        illumPositionsAllScans = np.append(illumPositionsAllScans, core_array_illum, axis=1)
    
    if numIllum != 0:
        return transPositionsAllScans, illumPositionsAllScans, time_taken
    else:
        return transPositionsAllScans, time_taken
    
    
def TransducerRotTrans(eff_x, eff_y, eff_z, eff_phi, eff_theta, R, homePath, Method = "trans"):
    """
    %%version 3: 20210331
    Takes the log file coordinates (one at a time, so loop if you want this for multiple scan points), calculates the centre of rotation, and applies the appropriate rotations to match the transducer positions happening in the scan.
    """
    
    if Method == 'Rascevska':
        x = eff_x - R*np.sin(np.radians(eff_theta))*np.cos(np.radians(eff_phi))
        y = eff_y - R*np.sin(np.radians(eff_theta))*np.sin(np.radians(eff_phi))
        z = eff_z - R*np.cos(np.radians(eff_theta))
        centre_rot = np.array([[x, y, z]])
        
        z_tr = z + R - 125
        transducer_pos = np.array([[x, y, z_tr]])
        transducer_pos = np.repeat(transducer_pos, 8, axis =0)
        transducer_pos = np.transpose(transducer_pos)
        u = [0, 0, 1]
        transducer_desired_afterphi = AxelRot(transducer_pos, eff_phi, u, centre_rot) #Rotate points for phi, going through centre of rotation
        u2 = np.squeeze(sph2cart(np.radians(eff_phi-90),0, 1)) #Create vector that is 90 deg from the current position of the array to set as rotation axis
        transducer_desired_aftertheta = AxelRot(transducer_desired_afterphi, -eff_theta, u2, centre_rot)#Rotate points for theta, going through centre of rotation
        transducer_pos_new = np.transpose(transducer_desired_aftertheta)
        return transducer_pos_new
    
    else:
        x = eff_x - R*np.sin(np.radians(eff_theta))*np.cos(np.radians(eff_phi))
        y = eff_y - R*np.sin(np.radians(eff_theta))*np.sin(np.radians(eff_phi))
        z = eff_z - R*np.cos(np.radians(eff_theta))
        centre_rot = np.array([[x, y, z]])
        
        try:
            import tables
            file = tables.open_file(homePath)
            if Method =="trans":
                transducer_pos_home = file.root.transducer_pos_home[:]
            elif Method =="illum":
                transducer_pos_home = file.root.transducer_pos_home[:]
            centre_rot_home = file.root.centre_rot_home[:]
        except:
            import scipy.io as sio
            homepos = sio.loadmat(homePath)
            if Method == "trans":
                transducer_pos_home = homepos.get("transducer_pos_home")
            elif Method == "illum":
                transducer_pos_home = homepos.get("illumination_pos_home")
            centre_rot_home = homepos.get("centre_rot_home")
                
        delta_cor = centre_rot - centre_rot_home
        transducer_pos = transducer_pos_home + delta_cor
        transducer_pos = np.transpose(transducer_pos)
        u = [0, 0, 1]
        transducer_desired_afterphi = AxelRot(transducer_pos, eff_phi, u, centre_rot) #Rotate points for phi, going through centre of rotation
        u2 = np.squeeze(sph2cart(np.radians(eff_phi-90),0, 1)) #Create vector that is 90 deg from the current position of the array to set as rotation axis
        transducer_desired_aftertheta = AxelRot(transducer_desired_afterphi, -eff_theta, u2, centre_rot)#Rotate points for theta, going through centre of rotation
        transducer_pos_new = np.transpose(transducer_desired_aftertheta)
        return transducer_pos_new

    
def sph2cart(azimuth, elevation, r):
    coselev = np.cos(elevation)
    x = eval("r * coselev * np.cos(azimuth)")
    y = eval("r * coselev * np.sin(azimuth)")
    z = eval("r * np.sin(elevation)")
    return x, y, z

def AxelRot(transducer_pos, thetadeg, u, centre_rot):
    """
    Modified from "https://stackoverflow.com/questions/6802577/rotation-of-3d-vector"
    "Euler-Rodrigues" method, author: unutbu

    Parameters
    ----------
    transducer_pos : Numpy array
        Array of home transducer positions.
    thetadeg : angle in degrees, 
        rotation defined as counter-clockwise using right-hand rule.
    u : Axis
        axis of rotation.
    centre_rot : CoR
        Point centre of rotation.

    Returns
    -------
    v_prime_vec_array : Array
        Returns the array with transducer positions shifted by the provided amounts.

    """
    v = transducer_pos
    v = (np.subtract(v,centre_rot.T)).T
    axis = u
    theta = np.radians(thetadeg)
    
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    rotation_matrix = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    Counter = 0
    v_prime_vec_array = np.zeros((np.shape(v)[0],3))
    for i in v:
        v_prime_vec_array[Counter,:] = np.dot(rotation_matrix, i)
        Counter = Counter +1
    v_prime_vec_array = np.transpose(np.add(v_prime_vec_array, centre_rot))
    return v_prime_vec_array


"""
    From  https://stackoverflow.com/questions/51272288/how-to-calculate-the-vector-from-two-points-in-3d-with-python
    for multiDimenDist and findVec
"""

def multiDimenDist(point1,point2):
    
   #find the difference between the two points, its really the same as below
   deltaVals = [point2[dimension]-point1[dimension] for dimension in range(len(point1))]
   runningSquared = 0
   #because the pythagarom theorm works for any dimension we can just use that
   for coOrd in deltaVals:
       runningSquared += coOrd**2
   return runningSquared**(1/2)

def findVec(point1,point2,unitSphere = False):
  #setting unitSphere to True will make the vector scaled down to a sphere with a radius one, instead of it's orginal length
  finalVector = [0 for coOrd in point1]
  for dimension, coOrd in enumerate(point1):
      #finding total differnce for that co-ordinate(x,y,z...)
      deltaCoOrd = point2[dimension]-coOrd
      #adding total difference
      finalVector[dimension] = deltaCoOrd
  if unitSphere:
      totalDist = multiDimenDist(point1,point2)
      unitVector =[]
      for dimen in finalVector:
          unitVector.append( dimen/totalDist)
      return unitVector
  else:
      return finalVector
  
    
"""From https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
For downloading Google Drive file
"""
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


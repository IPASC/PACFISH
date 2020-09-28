# -*- coding: utf-8 -*-
"""
Module to import log, data and transducer position files for PAI128 systems


Lawson Optics Lab
Lawson Health Research Institute
Western University
London, ON, Canada

Created by: Lawrence Yip
Last Modified 2020-09-28
"""


import numpy as np
from pathlib import Path
from numba import prange
import pandas as pd
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
        DESCRIPTION. basically unused

    """
    def fread(fidint, nelements, dtype):
        if dtype is np.str:
            dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
        else:
            dt = dtype
        data = np.fromfile(fidint, dt, nelements)

        if np.size(data) == 1:
            data = np.squeeze(data)
            if np.size(data) ==1:
                data = np.squeeze(data)
        return data
    
    fid = open(raw_data_filename, mode="rb")

    version = fread(fid,1,np.int16)
    UserID = fread(fid,1,np.int16)
    DAQsettingssize = fread(fid,1,np.int32)
    
    DAQsettings = {}
    
    for ii in range(DAQsettingssize):
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
        
    #Trakstar function
    tkEnabled = fread(fid,1,np.int8)
    if tkEnabled != 0:
        tkdatasize = fread(fid,1,np.int32)
        tkdata = fread(fid,6,np.double)
    else:
        tkdata = []
        
    fid.close()

    return UserID, DAQsettings, tkdata

def DAQ128settings2RF(DAQ128settings, CheckAveraging):
    if (DAQ128settings.get(0, {}).get("NumTriggers") > 1 and CheckAveraging == "True"):
        RFdata = np.zeros((len(DAQ128settings)*DAQ128settings.get(0, {}).get("NumChannels"), 
                       DAQ128settings.get(0, {}).get("NumPoints")*256),
                      dtype = np.single, order="F")
    else:
        RFdata = np.zeros((len(DAQ128settings)*DAQ128settings.get(0, {}).get("NumChannels"),
                       DAQ128settings.get(0, {}).get("NumPoints")*256*DAQ128settings.get(0, {}).get("NumTriggers")),
                      dtype = np.single, order="F")
        
    for ii in DAQ128settings:
        basen = ii * DAQ128settings.get(ii, {}).get("NumChannels")
        
        if  (DAQ128settings.get(ii, {}).get("NumTriggers") > 1 and CheckAveraging == "True"):
            temp = DAQ128settings.get(ii, {}).get("DataPoints")
            temp = temp.reshape(DAQ128settings.get(ii, {}).get("NumChannels"),-1, 
                                DAQ128settings.get(ii, {}).get("NumTriggers"),order="F")
            temp = np.mean(temp,2)
            
        else:
            temp = DAQ128settings.get(ii, {}).get("DataPoints")
            
        RFdata[(basen):(basen + DAQ128settings.get(ii, {}).get("NumChannels")),:] = temp
        
    return RFdata

def import_and_process_binary(raw_data_folder_path, num_scans, signal_inv=True, left_shift=12,
                 thresholding=0, photodiode=65, Averaging=True, end_remove=80, fluence_correc=False):
    
    #Determine initial values for sample length, number of channels, etc
    _, initial_values, _ = importPAI128(Path(raw_data_folder_path, "00000.pv3"))
    
    if Averaging == True:
        imData = np.zeros((num_scans, np.int32(initial_values.get(0, {}).get("NumPoints")*256/initial_values.get(0, {}).get("NumTriggers")), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    else:
        imData = np.zeros((num_scans, np.int32(initial_values.get(0, {}).get("NumPoints")*256), 
                          initial_values.get(0, {}).get("NumChannels")*len(initial_values)), dtype = np.single, order = "F")
    
    #Template to flip the signals since our transducers are all inverted in polarity
    reverseGain = -1 * np.ones((num_scans, 1),dtype = np.int, order = "F") 
    reverseGain[photodiode,:] = 1
    
    #Load the signals from the binary file
    AverageFluence = None
    do_not_fluence_correct = False
    for i in range(num_scans):
        count = str(i)
        S = Path(count.zfill(5)+".pv3")
        _, DAQsettings, _ = importPAI128(Path(raw_data_folder_path,S))
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
        
        if Averaging == False and initial_values.get(0, {}).get("NumTriggers") != 1:
            do_not_fluence_correct = True
            break
        else:
            #Remove last measurements (spikes)
            RFdata[(-end_remove):-1,:] = 0;    
            RFdata[-1,:] = 0;    
            #remove some at beginning and shift to align with laser Q-sync delay
            RFdata[0:left_shift+20,:] = 0;    
            RFdata = np.roll(RFdata,-left_shift,0)   
        
        if thresholding != 0:
            RFdata[abs(RFdata)<thresholding] = 0
            
        if fluence_correc == True and do_not_fluence_correct != False:
            if AverageFluence != None:
                break
            else:
                AverageFluence = np.max(np.mean(initial_values.get(0, {}).get("DataPoints").get(photodiode)))
            ShotPower = np.max(RFdata[0:(initial_values.get(0, {}).get("NumPoints")*256/initial_values.get(0, {}).get("NumTriggers")), photodiode])
            ShotRatio = AverageFluence/ShotPower
            RFadjusted = RFdata*ShotRatio
            RFdata = RFadjusted
        imData[i,:,:] = RFdata
        
    return RFdata

def load_scan_log(scan_log_file_path):
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
    R = 254.25 # Set length of arm between end effector and CoR for 360array
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
    transPositionsAllScans = np.zeros((64,3,numScans))
    for i in range(numScans):
        transPositionsAllScans[:,:,i] = TransducerRotTrans(scan_positions_abbrev[i,0], scan_positions_abbrev[i,1], scan_positions_abbrev[i,2],
                                                           scan_positions_abbrev[i,3], scan_positions_abbrev[i,4], scan_positions_abbrev[i,5])
    core_array = np.zeros((64,3,len(scan_positions_abbrev)))
    for j in range(len(scan_positions_abbrev)):
        cor_array_temp = np.reshape(np.tile(scan_positions_abbrev[j, 5:8],64),[3,-1],order="F")
        core_array[:,:,j] = cor_array_temp.T
    transPositionsAllScans = np.append(transPositionsAllScans, core_array,axis=1)
    return transPositionsAllScans, time_taken
    
    
def TransducerRotTrans(eff_x, eff_y, eff_z, eff_phi, eff_theta, R):
    """
    %%version 1
    Takes the log file coordinates (one at a time, so loop if you want this for multiple scan points), calculates the centre of rotation, and applies the appropriate rotations to match the transducer positions happening in the scan.
    """
    x = eff_x - R*np.sin(np.radians(eff_theta))*np.cos(np.radians(eff_phi))
    y = eff_y - R*np.sin(np.radians(eff_theta))*np.sin(np.radians(eff_phi))
    z = eff_z - R*np.cos(np.radians(eff_theta))
    centre_rot = np.array([[x, y, z]])
    
    try:
        import tables
        file = tables.open_file("20200311_Transducer_Position_Home.mat")
        transducer_pos_home = file.root.transducer_pos_home[:]
        centre_rot_home = file.root.centre_rot_home[:]
    except:
        import scipy.io as sio
        homepos = sio.loadmat("20200311_Transducer_Position_Home.mat")
        transducer_pos_home = homepos.get("transducer_pos_home")
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
    v_prime_vec_array = np.zeros((64,3))
    for i in v:
        v_prime_vec_array[Counter,:] = np.dot(rotation_matrix, i)
        Counter = Counter +1
    v_prime_vec_array = np.transpose(np.add(v_prime_vec_array, centre_rot))
    return v_prime_vec_array


"""
    From  https://stackoverflow.com/questions/51272288/how-to-calculate-the-vector-from-two-points-in-3d-with-python
    
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
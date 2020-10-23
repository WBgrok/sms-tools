import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import stft as STFT
import dftModel as DFT
import utilFunctions as UF


def computeEngEnvA(inputFile, window, M, N, H):
    (fs, x) = UF.wavread(inputFile)
    w = get_window(window, M, False)    
    (xmX, xpX) = STFT.stftAnal(x, w, N, H)
    #xmX = abs(10**(xmX_dB/20.0))         # convert from dB to linear magnitude
    #xmXl = xmX.copy()
    #xmXh = xmX.copy()
    fpb = fs/float(N)                    # freq step per bin for mX vectors
    L   = xmX[:,0].size                  # Get the number frames, L
    hN  = (N//2)+1                       # STFT uses DFTanal which returns only the psitive freq's
# ------------------------------------------------  Low Band    -----------------------------------------------------
    fcl = 3000.0                       # cutoff freq btw Low/Hi band
    Nfcl   = int(fcl/fpb)              # bin number corrsponding to 300Hz (actual freq @bin 69 = 2971Hz; w N =1024)  
    Xlow   = np.zeros(hN)            # Initialize Bin vector to hold low freq bins of active frame
    EnXlow = np.zeros(L)  
    print "Xlow size = %s" % Xlow.size             # Initialize Energy Env vector

# Low band loop
    for l in np.arange(L):
      Xlow = xmX[l, 1:Nfcl]            # Grab the low end of the current Frame
      Xlow = 10**(Xlow/20.0)           # 
      Xlow = abs(Xlow)  
      EnXlow[l] = np.sum(Xlow**2)      # capture the value of current Frame's energy  
      if l == 0:
        print EnXlow[l]
    print "Xlow size = %s" % Xlow.size
# ------------------------------------------------  High Band    -----------------------------------------------------
    fch = 10000.0                      # high freq cutoff   (upper limit of high band)
    Nfch = int(fch/fpb)                # bin number corrsponding to 10000Hz (bin )
    Xhi   = np.zeros(hN)      
    EnXhi = np.zeros(L)                     
      
 
# High Band loop
    for l in np.arange(L):
      Xhi = xmX[l, Nfcl+1:Nfch]       # Grab the Hi band:  300 < f < 10KHz spectrum lin mag of the current Frame  
      Xhi = 10**(Xhi/20.0)
      Xhi = abs(Xhi)
      EnXhi[l]  = np.sum(Xhi**2)  # capture the value of current Frame's energy
      if l == 0:
        print EnXhi[l]


    engEnv = np.zeros((L,2))

    # EnXlow[EnXlow<tol] = tol
    # EnXhi[EnXhi<tol]   = tol
    engEnv[:,0] = 10 * np.log10(EnXlow)
    engEnv[:,1] = 10 * np.log10(EnXhi)
    for k in ['Nfcl', 'Nfch', 'L']:
      print "%s = %s" %(k, locals()[k])

    return engEnv
    
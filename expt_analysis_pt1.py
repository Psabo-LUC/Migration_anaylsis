"""Check out cellmigration github repo"""

from datetime import datetime
import sys
import os
import shutil
sys.path.append("cellmigration")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import pims
import trackpy as tp
import tifffile
import cellmigration.expt_analysis.trackcells as tc
from config import config

CREATE_FILE_DUMP = False
DELETE_FILE_DUMP = True

#Define the path for dump folder
directory_name = "expt_analysis_pt1_dump_site"
dump_site = "/home/billb/Python Playground/"




user = "local"
#user = "remote"
if user == "local":
  name='1'
  useGdrive = False
  #path="/home/ekrueger2/microscopy_data/050124"
  #fileName=path+"/Position{}_050124.tif".format(name)
  fileName=f"{os.path.dirname(os.path.abspath(__file__))}/Position1_050124.tif"
elif user == "remote":
  name = "1" #
  name = "3"
  gpath=('/content/drive')
  path=gpath+"/MyDrive/public/"
  fileName = path+"/Position_%s_movie.tif"%name
  useGdrive=True
  sourcePath = "/content/cellmigration/"




if CREATE_FILE_DUMP == True:

    specific_path = dump_site + directory_name

    # Create the directory
    try:
        os.mkdir(specific_path)
        print(f"Directory '{specific_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{specific_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{specific_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

else: print("Dump creation disabled")
    

if CREATE_FILE_DUMP == True:

    raw_data = tifffile.imread(fileName)
    multichannel_check = raw_data.shape
    #print(multichannel_check)
    if multichannel_check[1] == 1:
        multiChannel = False
    else:
       multiChannel = True


    if multiChannel:
      channel=0
      frames=raw_data[:,channel,:,:]
    else:
      frames=raw_data[:,:,:]


    plt.imshow(frames[0,:,:])
    plt.savefig(os.path.join(dump_site, directory_name) + "/Cell_Map.png")


    """### Apply threshold to suppress background noise"""

    threshed = tc.ProcessFrames(frames,
                                downsampleRate=config.DOWN_SAMPLING,
                                crop=config.CROP,thresh=config.THRESHOLD)

    plt.imshow(threshed[0,:,:])
    plt.savefig(os.path.join(dump_site, directory_name) + "/Cell_Map_threshed.png")


    dummy = tc.TrialParams(threshed,refFrame=0,diameter=config.DIAMETER,minmass=config.MIN_MASS)
    if dummy.shape[0] <1:
      print("Error finding cells; try different parameters")
    else:
      finalStack = threshed

    def DoTracking(frames,diameter,minmass):
        """
        track particles using params determined from getParams()
        """
        fb = tp.batch(frames, diameter, minmass=minmass)
        return fb




    # run batch/tracking
    fb=tc.DoTracking(frames = finalStack,diameter=config.DIAMETER,minmass=config.MIN_MASS)

    plt.imshow(fb)
    plt.savefig(os.path.join(dump_site, directory_name) + "/" + f"Detected_cells_{datetime.now()}_diameter{config.DIAMETER}.png")



    try:
      print("shape final %d"%fb.shape[0])
    except:
      print("Unsuccessful tracking")
      #fb is a pandas record of coordinates, mass, signal strength, frame
    fb.to_csv(os.path.join(dump_site, directory_name) + "/Tracking_Output.csv")


    t = tp.link(fb,50 , memory=1)
    tp.plot_traj(t)

    plt.imshow(t)
    plt.savefig(os.path.join(dump_site, directory_name) + "/Tracking_Map.png")

else: print("CREATE_FILE_DUMP Global variable is set to False")

if DELETE_FILE_DUMP == True:
   path = os.path.join(dump_site, directory_name)
   shutil.rmtree(path)
else: print("DELETE_FILE_DUMP Global variable is set to False")
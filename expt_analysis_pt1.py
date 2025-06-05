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

CREATE_FILE_DUMP = True
DELETE_FILE_DUMP = False
BRIGHTFIELD = True



#Define the path for dump folder
directory_name = "expt_analysis_pt1_dump_site"
dump_site = "/home/billb/Python Playground/"


tif_name = "Position_1_background_editted"

user = "local"
#user = "remote"
if user == "local":
  name='1'
  useGdrive = False
  #path="/home/ekrueger2/microscopy_data/050124"
  #fileName=path+"/Position{}_050124.tif".format(name)
  fileName=f"{os.path.dirname(os.path.abspath(__file__))}/{tif_name}.tif"
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
    #print(len(multichannel_check))
    if len(multichannel_check) == 3:
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
    if BRIGHTFIELD == False:
      threshed = tc.ProcessFrames(frames,
                                  downsampleRate=config.DOWN_SAMPLING,
                                  crop=config.CROP,thresh=config.THRESHOLD)
    else:
      threshed = frames
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
    fb=tc.DoTracking(frames = finalStack, diameter=config.DIAMETER, minmass=config.MIN_MASS)
    #plt.imshow(fb)
    #plt.savefig(os.path.join(dump_site, directory_name) + "/" + f"Detected_cells_{datetime.now()}_diameter{config.DIAMETER}.png")



    try:
      print("shape final %d"%fb.shape[0])
    except:
      print("Unsuccessful tracking")
      #fb is a pandas record of coordinates, mass, signal strength, frame
    #fb.to_csv(os.path.join(dump_site, directory_name) + "/Tracking_Output.csv")
    


    t = tp.link(fb, search_range = config.MAX_DIST, memory=config.MAX_MISSED_FRAME)
    t_reindexed = t.set_index('frame')
    #print(t)
    plt.figure(figsize=(30,30))
    tp.plot_traj(traj = t, label = True)
    plt.savefig(os.path.join(dump_site, directory_name) + "/Trajectory_Map.png")

    plt.figure(figsize=(30,30))
    tp.plot_traj(traj = t, superimpose = frames[0,:,:], label = True)
    plt.savefig(os.path.join(dump_site, directory_name) + "/Tracking_Map.png")
    t_reindexed.to_csv(os.path.join(dump_site, directory_name) + f"/Tracking_Output_{tif_name}.csv")


    def split_by_particle_sorted(df):
      grouped = df.groupby('particle')
      return dict(map(lambda kv: (int(kv[0]), kv[1][['x', 'y']].sort_index().copy()), grouped))

    trajectory_sorted = split_by_particle_sorted(t_reindexed)
    print(trajectory_sorted[0])

    def track_checking(trajectories, leading_particle, end_particle, show_frame_pngs = False, show_particle_traj_data = True):
      if show_particle_traj_data == True:
         print(f"Leading traj:{trajectories[leading_particle]}")
         print(f"Ending traj:{trajectories[end_particle]}")
      else:print("Set 'show_particle_traj_data' to True to display frame by frame positions")

      if show_frame_pngs == True:
        for j in range(config.VIDEO_LENGTH):
          plt.figure(figsize=(20,20))
          fig=plt.figure(figsize=(20,20))
          #ax=fig.add_subplot(222)
          
          xs0 = trajectories[leading_particle]['x']
          ys0 = trajectories[leading_particle]['y']
          plt.plot(xs0, ys0, lw = 0.6)
          plt.imshow(frames[j,:,:],cmap='Greys')
          #plt.savefig(os.path.join(dump_site, directory_name) + "/Leading_Map.png")

          
          xs1 = trajectories[end_particle]['x']
          ys1 = trajectories[end_particle]['y']
          plt.plot(xs1, ys1, lw = 0.6)
          #plt.imshow(frames[0,:,:],cmap='Greys')
          plt.savefig(os.path.join(dump_site, directory_name) + f"/Traj_Map_Frame_{j}.png")
      else: print("Set 'Show_frame_pngs' = True to generate frame maps")
      return 
    

    #point_cords = (frame, x, y) of point to add
    #state = active or testing
    def track_manipulation(trajectories, leading_particle, end_particle, operation, state, point_cords):
      if operation == "merge":
         print("'merge' not yet added")

      elif operation == "delete_particle":   
         print("'delete_particle' not yet added")

      elif operation == "add_point":
        cords = {'x':[point_cords[1]], 'y':[point_cords[2]]}
        cords_df = pd.DataFrame(data = cords)
        x = cords_df['x']
        y = cords_df['y']
        plt.figure(figsize=(20,20))
        fig=plt.figure(figsize=(20,20))
        plt.imshow(frames[point_cords[0],:,:],cmap='Greys')
        plt.plot(x, y, 'o')
        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Frame_{point_cords[0]}.png")

        if point_cords[0] == (len(trajectories[leading_particle]-1)):
          print("Coordinates for this frame currently exist")
        elif(point_cords[0] - (len(trajectories[leading_particle]-1))) == 1:
          print("Coordinates for this frame do not exist")
          if state == "active":
            plt.figure(figsize=(20,20))
            fig=plt.figure(figsize=(20,20))
            plt.imshow(frames[point_cords[0],:,:],cmap='Greys')
            xs0 = trajectories[leading_particle]['x'].copy()
            ys0 = trajectories[leading_particle]['y'].copy()
            plt.plot(xs0, ys0, lw = 0.6)
            plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Before.png")

            trajectories[leading_particle] = pd.concat([trajectories[leading_particle],cords_df], ignore_index=True)
            
            xs1 = trajectories[leading_particle]['x']
            ys1 = trajectories[leading_particle]['y']
            plt.plot(xs1, ys1, lw = 0.6)
            plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_After.png")

          elif state == "testing":
            plt.figure(figsize=(20,20))
            fig=plt.figure(figsize=(20,20))
            plt.imshow(frames[point_cords[0],:,:],cmap='Greys')
            xs0 = trajectories[leading_particle]['x']
            ys0 = trajectories[leading_particle]['y']
            plt.plot(xs0, ys0, lw = 0.6)
            plt.plot(x, y, 'o')
            plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Test.png")
            print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")
         #print("'add_point' not yet added")
      elif operation == "delete_point":
        print("'delete_point' not yet added")
      else: print("Function could not understand operation input") 
      return trajectories 

    #track_checking(trajectories = trajectory_sorted, leading_particle = 8, end_particle = 141)

    trajectories = track_manipulation(trajectories = trajectory_sorted, leading_particle = 8, end_particle = 141, operation = "add_point", state = "testing", point_cords = (15, 674, 1446))
       
    track_checking(trajectories, leading_particle = 8, end_particle = 141)







else: print("CREATE_FILE_DUMP Global variable is set to False")









if DELETE_FILE_DUMP == True:
   path = os.path.join(dump_site, directory_name)
   shutil.rmtree(path)
else: print("DELETE_FILE_DUMP Global variable is set to False")
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

directory_name = "expt_analysis_pt1_dump_site"
dump_site = "/home/billb/Python Playground/"

tif_file = "Position_1_background_editted"

fileName = f"{os.path.dirname(os.path.abspath(__file__))}/{tif_file}.tif"
Tracking_output = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/Tracking_Output_{tif_file}.csv")

t_reindexed = Tracking_output.set_index('frame')

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



def split_by_particle_sorted(df):
    grouped = df.groupby('particle')
    return dict(map(lambda kv: (int(kv[0]), kv[1][['x', 'y']].sort_index().copy()), grouped))

trajectory_sorted = split_by_particle_sorted(t_reindexed)
#print(trajectory_sorted[0])


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
       
trajectories.to_csv(os.path.join(dump_site, directory_name) + f"/Tracking_Output_{tif_file}.csv")

track_checking(trajectories, leading_particle = 8, end_particle = 141)
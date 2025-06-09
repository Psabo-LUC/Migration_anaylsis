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
dump_site = f"{os.path.dirname(os.path.abspath(__file__))}/"
tif_file = "Position_1_background_editted"
fileName = f"{os.path.dirname(os.path.abspath(__file__))}/{tif_file}.tif"

Tracking_output = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/Tracking_Output_{tif_file}.csv")

#print(f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/Testing.csv")

while os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/Testing.csv") == True:
    Tracking_output = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/Testing.csv")
    print("Using testing csv")
    break

    


#print(Tracking_output)

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


#print(trajectory_sorted[0])


def track_checking(trajectories, leading_particle, end_particle, ref_frame = 0,  show_frame_pngs = False, show_particle_traj_data = True):
    if ((leading_particle in trajectories) and (end_particle in trajectories)) == True:
        if show_particle_traj_data == True:
            print(f"Leading traj:{trajectories[leading_particle]}")
            print(f"Ending traj:{trajectories[end_particle]}")
        else:
            print("Set 'show_particle_traj_data' to True to display frame by frame positions")

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

    elif (leading_particle in trajectories) == False:
        print("Leading particle does not exist")
    elif (end_particle in trajectories) == False:
        print("Ending particle does not exist")
    elif (leading_particle in trajectories == False) and (end_particle in trajectories == False) == True:
        print("Neither Particle exists")
    return 


    #point_cords = (frame, x, y) of point to add
    #state = active or testing
def track_manipulation(trajectories, leading_particle, end_particle, operation, state, point_cords, ref_frame):
    if (leading_particle in trajectories) and (end_particle in trajectories):
        if operation == "merge":
            if state == "active":
                leading_traj = trajectories[leading_particle]
                ending_traj = trajectories[end_particle]
                trajectories[leading_particle] = pd.concat([leading_traj,ending_traj], ignore_index=True)
                del trajectories[end_particle]
                print(f"Particle:{leading_particle} has been merged with Particle:{end_particle}. Particle:{end_particle} has been deleted from trajectory list")
            elif state == "testing":
                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                leading_traj = trajectories[leading_particle]
                ending_traj = trajectories[end_particle]
                x0 = leading_traj['x']
                y0 = leading_traj['y']
                x1 = ending_traj['x']
                y1 = ending_traj['y']
                plt.plot(x0, y0, lw = 0.6, c = 'red')
                plt.plot(x1, y1, lw = 0.6, c = 'blue')
                plt.savefig(os.path.join(dump_site, directory_name) + "/Track_manipulation_Map_Before.png")

                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                testing_trajectories = pd.concat([leading_traj,ending_traj], ignore_index=True)
                x = testing_trajectories['x']
                y = testing_trajectories['y']
                plt.plot(x, y, lw = 0.6)
                plt.savefig(os.path.join(dump_site, directory_name) + "/Track_manipulation_Map_After.png")
                print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")



        elif operation == "delete_particle":
            if state == "active":
                del trajectories[leading_particle]
                print(f"Particle:{leading_particle} has been deleted from trajectory list")
                
            elif state == "testing":
                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                xs0 = trajectories[leading_particle]['x']
                ys0 = trajectories[leading_particle]['y']
                plt.plot(xs0, ys0, lw = 0.6)
                plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Before.png")

                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                trajectories_del = trajectories.copy()
                del trajectories_del[leading_particle]
                plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_After.png")
                print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")
        elif operation == "add_point":
            cords = {'x':[point_cords[1]], 'y':[point_cords[2]]}
            cords_df = pd.DataFrame(data = cords).set_index([[point_cords[0]]])
            x = cords_df['x']
            y = cords_df['y']
            plt.figure(figsize=(20,20))
            fig=plt.figure(figsize=(20,20))
            plt.imshow(frames[ref_frame,:,:],cmap='Greys')
            plt.plot(x, y, 'o')
            plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Frame_{point_cords[0]}.png")

            if (point_cords[0] in trajectories[leading_particle].index):
                print("Coordinates for this frame currently exist")
            elif (point_cords[0] in trajectories[leading_particle].index) and ((point_cords[0]-1) in (trajectories[leading_particle].index)):
                print("This is a dangling point, add prior frames before adding this one")
            elif (point_cords[0] not in trajectories[leading_particle].index):
                if (((point_cords[0]-1) not in trajectories[leading_particle].index) and ((point_cords[0]+1) not in trajectories[leading_particle].index)):
                    print("This is a dangling point, add prior frames before adding this one")
                elif ((point_cords[0]-1) in trajectories[leading_particle].index):
                    print("Coordinates for this frame do not exist but a preceeding point exists")
                    if state == "active":
                        plt.figure(figsize=(20,20))
                        fig=plt.figure(figsize=(20,20))
                        plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                        xs0 = trajectories[leading_particle]['x'].copy()
                        ys0 = trajectories[leading_particle]['y'].copy()
                        plt.plot(xs0, ys0, lw = 0.6)
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Before.png")

                        trajectories[leading_particle] = pd.concat([trajectories[leading_particle],cords_df], ignore_index=False)

                        xs1 = trajectories[leading_particle]['x']
                        ys1 = trajectories[leading_particle]['y']
                        plt.plot(xs1, ys1, lw = 0.6)
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_After.png")
                        print(f"Particle:{leading_particle} has been updated")

                    elif state == "testing":
                        plt.figure(figsize=(20,20))
                        fig=plt.figure(figsize=(20,20))
                        plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                        xs0 = trajectories[leading_particle]['x']
                        ys0 = trajectories[leading_particle]['y']
                        plt.plot(xs0, ys0, lw = 0.6)
                        plt.plot(x, y, 'o')
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Test.png")
                        print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")
                     #print("'add_point' not yet added")
                elif ((point_cords[0]+1) in trajectories[leading_particle].index):
                    print("Coordinates for this frame do not exist but a proceeding point exists")
                    if state == "active":
                        plt.figure(figsize=(20,20))
                        fig=plt.figure(figsize=(20,20))
                        plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                        xs0 = trajectories[leading_particle]['x'].copy()
                        ys0 = trajectories[leading_particle]['y'].copy()
                        plt.plot(xs0, ys0, lw = 0.6)
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Before.png")

                        trajectories[leading_particle] = pd.concat([cords_df,trajectories[leading_particle]], ignore_index=False)

                        xs1 = trajectories[leading_particle]['x']
                        ys1 = trajectories[leading_particle]['y']
                        plt.plot(xs1, ys1, lw = 0.6)
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_After.png")
                        print(f"Particle:{leading_particle} has been updated")

                    elif state == "testing":
                        plt.figure(figsize=(20,20))
                        fig=plt.figure(figsize=(20,20))
                        plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                        xs0 = trajectories[leading_particle]['x']
                        ys0 = trajectories[leading_particle]['y']
                        plt.plot(xs0, ys0, lw = 0.6)
                        plt.plot(x, y, 'x')
                        plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Test.png")
                        print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")

        elif operation == "delete_point":
            if state == "active":
                trajectories[leading_particle] = trajectories[leading_particle].drop(labels = point_cords[0], axis = 0)
                print(f"Frame:{point_cords[0]} of Particle:{leading_particle} has been deleted")

            elif state == "testing":
                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                xs0 = trajectories[leading_particle]['x']
                ys0 = trajectories[leading_particle]['y']
                plt.plot(xs0, ys0, lw = 0.6)
                plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_Before.png")

                plt.figure(figsize=(20,20))
                fig=plt.figure(figsize=(20,20))
                plt.imshow(frames[ref_frame,:,:],cmap='Greys')
                traj_test = trajectories[leading_particle].copy()
                traj_test = traj_test.drop(labels = point_cords[0], axis = 0)
                xs0 = traj_test['x']
                ys0 = traj_test['y']
                plt.plot(xs0, ys0, lw = 0.6)
                plt.savefig(os.path.join(dump_site, directory_name) + f"/Track_manipulation_Map_After.png")






                print("Set 'state' function variable to 'active' for the operation to be applied to the leading particle. This is a safety feature, 'state' should be set to 'testing' unless the user is completely confident in the operations outcome")

                
            print("'delete_point' not yet added")
        else: print("Function could not understand operation input") 
    elif leading_particle in trajectories == False:
        print("Leading particle does not exist")
    elif end_particle in trajectories == False:
        print("Ending particle does not exist")
    elif (leading_particle in trajectories == False) and (end_particle in trajectories == False):
        print("Neither Particle exists")
    return trajectories 


def data_unpacking(trajectories):
    unpacked_traj = pd.DataFrame()
    for particle in list(trajectories.keys()):
        sub_df = pd.DataFrame(trajectories[particle])
        sub_df.insert(2, 'particle', particle)
        reindex_sub_df = sub_df.reset_index()
        reindex_sub_df = reindex_sub_df.rename(columns = {"index":"frame"})
        unpacked_traj =pd.concat([unpacked_traj,reindex_sub_df])
    unpacked_traj = unpacked_traj.sort_values(by =['frame','particle'])
    unpacked_traj = unpacked_traj.reset_index(drop = True)
    return unpacked_traj

def traj_map(trajectory, ref_frame = 0):
    t = trajectory 
    plt.figure(figsize=(30,30))
    tp.plot_traj(traj = t, label = True)
    plt.imshow(frames[ref_frame,:,:],cmap='Greys')
    plt.savefig(os.path.join(dump_site, directory_name) + "/Trajectory_Map_updated.png")
    return







trajectory_sorted = split_by_particle_sorted(t_reindexed)


track_checking(trajectories = trajectory_sorted, leading_particle =103, end_particle = 138,  ref_frame =9)

trajectories = track_manipulation(trajectories = trajectory_sorted, leading_particle = 103, end_particle = 138, ref_frame = 0, operation = "add_point", state = "testing", point_cords = (0, 2028, 546))


#track_checking(trajectories, leading_particle =8, end_particle = 141)



editted_trajs = data_unpacking(trajectories)
traj_map(trajectory = editted_trajs, ref_frame = 10)
editted_trajs.to_csv(os.path.join(dump_site, directory_name) + "/Testing.csv")

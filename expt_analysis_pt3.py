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
import cellmigration.expt_analysis.trackcells as tc
from config import config



#NAME = "1" #number used to labal files 

PATH_1 = f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/"
FILE_1 = "Testing.csv"

FILEPATH_1 = PATH_1 + FILE_1

PATH_2 = f"{os.path.dirname(os.path.abspath(__file__))}/expt_analysis_pt1_dump_site/"
FILE_2 = "Tracking_Output.csv"

FILEPATH_2 = PATH_2 + FILE_2


DATA_1 = pd.read_csv(FILEPATH_1)
DATA_1_TESTING = DATA_1.copy()
DATA_1_TESTING = DATA_1_TESTING.set_index('frame')


DATA_2 = pd.read_csv(FILEPATH_2)
DATA_2_TESTING = DATA_2.copy()
DATA_2_TESTING = DATA_2_TESTING.set_index('frame')

CREATE_FILE_DUMP = True
DELETE_FILE_DUMP = False

directory_name = "expt_analysis_pt3_dump_site"
dump_site = f"{os.path.dirname(os.path.abspath(__file__))}/"

OUTPUT_DATA_PATH =f"{os.path.dirname(os.path.abspath(__file__))}/Data_dump/"
OUTPUT_DATA_FILE = "Well_8_100uM_ATP"
OUTPUT_DATA_FILEPATH = OUTPUT_DATA_PATH + OUTPUT_DATA_FILE





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



















def stub_removal(linked_data):
    linked_data_trimmed = tp.filter_stubs(linked_data, 5)
    return linked_data_trimmed
  

def split_by_particle_sorted(df):
  grouped = df.groupby('particle')
  return dict(map(lambda kv: (int(kv[0]), kv[1][['x', 'y']].sort_index().copy()), grouped))

def Particle_Average_Velocity(particle_dfs2):
  Particle_IDs = list(particle_dfs2.keys())
  packaged_displacement_data = dict()
  packaged_velocity_data = dict()
  AVG_VELs = []

  for Particles in list(range(len(particle_dfs2.keys()))):
    dframe_change = []
    individual_magnitude_stacked = []
    velocity = []


    for frame_IDs in list(range(len(particle_dfs2[Particle_IDs[Particles]]))):
      x0, y0 = particle_dfs2[Particle_IDs[Particles]].iloc[frame_IDs-1][['x', 'y']]
      x1, y1 = particle_dfs2[Particle_IDs[Particles]].iloc[frame_IDs][['x', 'y']]
      dframe_end = int(particle_dfs2[Particle_IDs[Particles]].index[frame_IDs])
      dframe_start = int(particle_dfs2[Particle_IDs[Particles]].index[frame_IDs-1])
      dframe = (dframe_end - dframe_start)*config.FRAME_RATE*((1/60)*(1/60)) #Length of time between frames and converted to hours
      dframe_change.append(dframe)
      dx = x1 - x0
      dy = y1 - y0
      indiv_magnitude = np.sqrt(dx**2 + dy**2)*config.PIXEL_SIZE
      individual_magnitude_stacked.append(indiv_magnitude)
      vel = indiv_magnitude/dframe
      velocity.append(vel)
      velocity_stack = pd.DataFrame(velocity, columns = ["Velocity(um/hr)"])
      time_stack = pd.DataFrame(dframe_change,columns = ["Time(hr)"])
      distance_stack = pd.DataFrame(individual_magnitude_stacked, columns = ["Distance(um)"])
    AVG_VEL = velocity_stack.mean(axis = 0)
    #print(AVG_VEL)
    AVG_VELs.append(float(AVG_VEL.iloc[0]))
    merged = pd.concat([time_stack,distance_stack,velocity_stack], axis = 1)
    merged_corrected = merged.truncate(before=1, axis=0)
    packaged_displacement_data[f"{Particle_IDs[Particles]}"] = merged_corrected

  AVG_VEL_stack = pd.DataFrame(AVG_VELs, columns = ["Average_Velocity(um/hr)"], index = Particle_IDs)
  AVG_VEL_stack.index.name = 'Particle'

  return packaged_displacement_data, AVG_VEL_stack





#velocity Histograms

DATA_1_SORTED = split_by_particle_sorted(DATA_1_TESTING)
AVE = Particle_Average_Velocity(particle_dfs2 = DATA_1_SORTED)
fig=plt.figure(figsize=(20,20))
plt.hist(x = AVE[1], bins = 20)
plt.savefig(os.path.join(dump_site, directory_name) + f"/Velo_histo_1.png")



#DATA_2_SORTED = split_by_particle_sorted(DATA_2_TESTING)
#AVE = Particle_Average_Velocity(particle_dfs2 = DATA_2_SORTED)
#fig=plt.figure(figsize=(20,20))
#plt.hist(x = AVE[1], bins = 20)
#plt.savefig(os.path.join(dump_site, directory_name) + f"/Velo_histo_2.png")


#MSD Calcualtions
def drift_correction(data):
  drift = tp.compute_drift(data)
  data_drift_corrected = tp.subtract_drift(data.copy(), drift)
  data_drift_corrected.plot()
  plt.show()
  plt.savefig(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/Drift_{name}_map.png")
  return data_drift_corrected


def doMSDFit(
  average_MSD_files,
  #fittingRange = [0,100]
  fittingRange=None
  ):
  """
  fits MSD to input csv files
  """
  
  for file, info in average_MSD_files.items():
      df = pd.read_csv(file)
      plt.errorbar(df['lagt'], df['msd'], yerr=np.std(df['msd']), label=f'{file}', color=info["color"])
      if fittingRange is not None:
        sub = df.iloc[0:fittingRange[1]]
      else:
        sub = df
      lagt = sub['lagt']
      msd = sub['msd']
      fit_coefficients = np.polyfit(lagt, msd, 1)
      linear_fit = np.poly1d(fit_coefficients)
      plt.plot(df['lagt'], linear_fit(df['lagt']), label=f'{file} - Linear Fit', linestyle='--', color=info["color"])


  plt.xlabel('lagt')
  plt.ylabel('msd')
  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  plt.title('Average MSD with Standard Deviation and Linear Fit')
  MSD_output = pd.DataFrame(fit_coefficients)
  MSD_output.to_csv(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/Slope_intercept_{name}.csv")
  print("slope/intercept",fit_coefficients)














def drift_no_drift_MSD_plot(Data_no_drift_correction, Data_drift_corrected):
  em_with_drift = tp.emsd(Data_no_drift_correction, config.PIXEL_SIZE, 1/config.FRAME_RATE, max_lagtime = config.MAX_LAG_TIME)
  em_drift_corrected = tp.emsd(Data_drift_corrected, config.PIXEL_SIZE, 1/config.FRAME_RATE, max_lagtime = config.MAX_LAG_TIME)

  fig, ax = plt.subplots()
  cmap = plt.colormaps.get_cmap('CMRmap')
  ax.plot(em_drift_corrected.index, em_drift_corrected, 'k', color=cmap(100), label = 'MSD drift corrected')
  ax.plot(em_with_drift.index, em_with_drift, 'k', color=cmap(1), label = 'MSD non-drift corrected')
  ax.set(ylabel=r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]',
       xlabel='time ($sec$)')
  ax.set(xlim=(0, max(em_drift_corrected.index)));
  ax.set(ylim=(0, max(em_drift_corrected)));
  ax.legend(fontsize=7)
  plt.savefig(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/MSD_Drift_nonDrift_{name}_plot.png")
  return em_with_drift, em_drift_corrected



def slope_intercept(data):
  ts,traj,msd,im,em=tc.DoMSD(
    data,
    maxDist=config.MAX_DIST, # maximum displacement between frames in pixel
    maxMissFrame=config.MAX_MISSED_FRAME, # allowed number of frames a particle can disappear
    minFrame=config.MIN_FRAME, # minimum number of frames a trajectory needs to last
    pixelSize=config.PIXEL_SIZE, # image pixel size in micron/pixel, specific for each scope and lens (Cytiva 10X: 0.65) and (Spinning Disk: 1.1 at 10X)
    frameRate=1/config.FRAME_RATE, # image acquisition rate in frames/sec
    max_lagtime=config.MAX_LAG_TIME, # intervals of frames out to which MSD is computed
    name=name
)
  # get displacements
  dists, xdists = tc.CalcDistances(traj) # performed on trajectories BEFORE drift-correction
  med = np.median(xdists)
  plt.figure()
  plt.title("%f median displacement"%med)
  plt.hist(xdists,label="displacements")
  plt.legend(loc=0)
  plt.savefig(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/Displacment_{name}_histo.png")

# save average MSD for each run to csv file
  msdFileName=OUTPUT_DATA_FILEPATH+f'averageEM_{name}.csv'
  diffFileName=OUTPUT_DATA_FILEPATH+f'diff_{name}.csv'
  if name is not None:
    em.to_csv(msdFileName)
    np.savetxt(diffFileName,np.array(xdists))
    # prompt: save pandas dataframe
    traj.to_csv(OUTPUT_DATA_FILEPATH+f'/traj_{name}.csv')
    data.to_csv(OUTPUT_DATA_FILEPATH+f'/fbframe_{name}.csv')

  msdFile={
    OUTPUT_DATA_FILEPATH+f'averageEM_{name}.csv':{"color":"blue"}
}
  plt.figure()
  doMSDFit(msdFile, fittingRange=config.FITTING_RANGE)
  plt.savefig(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/MSD_f{name}_plot.png")
  return

#individual MSDs? save figures?




Files = 10

for File in range(1, Files, 1):
#for File in Files:
  name = File 
  csv_name = f"Tracking_Output_Position_{name}_background_editted"
  fileName= f"{os.path.dirname(os.path.abspath(__file__))}/Data_dump/{OUTPUT_DATA_FILE}/{csv_name}.csv"
  data_input = pd.read_csv(fileName)
  data_input_destubbed = stub_removal(linked_data = data_input)
  data_input_dict = split_by_particle_sorted(data_input_destubbed)
  dis_ave = Particle_Average_Velocity(particle_dfs2 = data_input_dict)

  fig=plt.figure(figsize=(20,20))
  plt.hist(x = dis_ave[1], bins = 20)
  plt.savefig(os.path.join(OUTPUT_DATA_PATH, OUTPUT_DATA_FILE) + f"/Velo_histo_{name}.png")

  data_drift_corrected = drift_correction(data = data_input_destubbed)

  drift_no_drift_MSD_plot(Data_no_drift_correction =data_input_destubbed, Data_drift_corrected =data_drift_corrected)
  
  slope_intercept(data = data_input)



















if DELETE_FILE_DUMP == True:
   path = os.path.join(dump_site, directory_name)
   shutil.rmtree(path)
else: print("DELETE_FILE_DUMP Global variable is set to False")



#em_set = drift_no_drift_MSD_plot(Data_no_drift_correction = DATA_1, Data_drift_corrected = drift_correction(data = DATA_1))





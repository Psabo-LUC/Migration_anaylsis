This is the most recently updated and functioning script to determine characteristics of BV2 cell migration.

This script was built to take in Tagged Image Files(.TIF) as its input. 

Currently, this script is divided into two parts (that may get partitioned in later versions) where the first part can calculate and output the following:

- .TIF postprocessing (intensity thresholding and diameter/Mass of intensity exclusion) to deteremine individual cells pixel coordinates
- Using Trackpy(https://github.com/soft-matter/trackpy), the individual cell coordinates are mapped together across all frames of the .TIF stack to generate trajectory maps which are stored in a dict(Particle_ID:Trajectory_data) data type/format



Using this data in the second part of this script, several directional and spacial analysis are done on each particle to determine and generate the following:
  - Particles frame count:
    ![Particle frame duration](https://github.com/user-attachments/assets/ab6fcbd4-7bdf-4b58-97df-2bc6d5569885)
  - Histograms displaying frequancy of the average velocity:
    ![Velocity Histogram](https://github.com/user-attachments/assets/c8dc55b9-691a-425d-b4f1-e81d66e36f4d)
  - Individual cell trajectory maps labeled with the particle_ID, displacement (between the initial and final frames of detection), and velocity
    ![Trajectory_displacement_maps](https://github.com/user-attachments/assets/66570264-3f8b-44a3-b373-544c95df9c53)
  - Mapping normalized displacements into polar coordinates/angles and divides cells into groups based off percent displacement relative to the maximum normalized vector(Short:0.33-0, Medium:0.66-0.34, Long:0.67-1). Afterwhich, the left vs. right cell displacements are counted and displayed. The purpose of this analysis is to see if there is a noticable deviation in cell directionaility based off of the cell total displacement
    ![Short_norms](https://github.com/user-attachments/assets/71596dc7-c418-4f1e-821e-01eb7492876b)
    ![Medium_norms](https://github.com/user-attachments/assets/014d2910-d9b4-4822-8c28-252be6dfa36e)
    ![Long_norms](https://github.com/user-attachments/assets/c874d3af-db88-4215-ad29-cd0e077be60c)
  - Averaged X and Y drift values from all cells based on frame (used to determine coefficient of drift correction) 
    ![X&Y_Drift](https://github.com/user-attachments/assets/8d626168-b48c-408f-96d2-7452a7df4f43)
  - Calcualtion of Mean Squared Displacement(MSD) of all detected particles both before, and after subtraction of the drift coefficient from each cells. Plotted as MSD vs. Time
    ![MSD](https://github.com/user-attachments/assets/8317ce12-aab8-457f-a4c8-d277a2db0190)
  - Using Linear regression to determine the slope and intercept of the initially linear region of the MSD vs. Time plot. This linear region is where the cells motion is assumed to be equatable to Brownian motion. As a result of this assumption of Brownain motion, the diffusion coeffient can be determined using the equation {\displaystyle {\text{MSD}}=2nDt.}
    ![MSD Linear fit](https://github.com/user-attachments/assets/4181d01b-6ce4-461c-b4e0-cd31885851d3)


NOTES: 
- There are additional features that live inside of this script that are relics from previous users, these features have not been tested by me and will get added/removed/changed as I refactor this script.





    


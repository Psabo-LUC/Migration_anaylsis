This is the most recently updated and functioning script to determine characteristics of BV2 cell migration.

This script was built to take in Tagged Image Files(.TIF) as its input. 

Currently, this script is divided into two parts (that may get partitioned in later versions) where the first part can calculate and output the following:

- .TIF postprocessing (intensity thresholding and diameter/Mass of intensity exclusion) to deteremine individual cells pixel coordinates
- Using Trackpy(https://github.com/soft-matter/trackpy), the individual cell coordinates are mapped together across all frames of the .TIF stack to generate trajectory maps which are stored in a dict(Particle_ID:Trajectory_data) data type/format



Using this data in the second part of this script, several directional and spacial analysis are done on each particle to determine and generate the following:
  - Particles frame count:
    ![Particle frame duration](https://github.com/user-attachments/assets/ab6fcbd4-7bdf-4b58-97df-2bc6d5569885)
    
  - Histograms displaying frequancy of the average velocity:
    ![Velocity Histogram](https://github.com/user-attachments/assets/e250fbeb-a8e1-4fdb-a5b9-6e121cf1c3e5)
    
  - Individual cell trajectory maps labeled with the particle_ID, displacement (between the initial and final frames of detection), and velocity
    ![Trajectory_displacement_maps](https://github.com/user-attachments/assets/66570264-3f8b-44a3-b373-544c95df9c53)
    
  - Mapping normalized displacements into polar coordinates/angles and divides cells into groups based off percent displacement relative to the maximum normalized vector(Short:0.33-0, Medium:0.66-0.34, Long:0.67-1). Afterwhich, the left vs. right cell displacements are counted and displayed. The purpose of this analysis is to see if there is a noticable deviation in cell directionaility based off of the cell total displacement
    
    ![Short_norms](https://github.com/user-attachments/assets/71596dc7-c418-4f1e-821e-01eb7492876b)
    ![Medium_norms](https://github.com/user-attachments/assets/014d2910-d9b4-4822-8c28-252be6dfa36e)
    ![Long_norms](https://github.com/user-attachments/assets/c874d3af-db88-4215-ad29-cd0e077be60c)
    
  - Averaged X and Y drift values from all cells based on frame (used to determine coefficient of drift correction)
    
    ![X&Y_Drift](https://github.com/user-attachments/assets/8d626168-b48c-408f-96d2-7452a7df4f43)
    
  - Calcualtion of Mean Squared Displacement(MSD) of all detected particles both before, and after subtraction of the drift coefficient from each cells. Plotted as MSD vs. Time
    
    ![MSD](https://github.com/user-attachments/assets/f8e8898d-d98f-4171-ae1d-27b0a8800cc7)
    
  - Using Linear regression to determine the slope and intercept of the initially linear region of the MSD vs. Time plot. This linear region is where the cells motion is assumed to be equatable to Brownian motion. As a result of this assumption of Brownain motion, the diffusion coeffient can be determined using the equation
     ![MSD equation](https://github.com/user-attachments/assets/f7b0fe9c-6167-4cad-b9e6-4a726d7238be)

     ![image](https://github.com/user-attachments/assets/ebe93599-f9dd-453f-845a-5f14b469a847)



NOTES: 
- There are additional features that live inside of this script that are relics from previous users, these features have not been tested by me and will get added/removed/changed as I refactor this script.





    


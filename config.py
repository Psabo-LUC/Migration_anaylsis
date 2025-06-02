class Config:
    #TIFF file post processing
    FRAME_RATE = 180 #second/frames
    DOWN_SAMPLING= 0
    CROP=[[0,1000],[0,1000]]
    THRESHOLD=110


    #Valid cell parameters 
    DIAMETER=101
    MIN_MASS=15000

    # for fitting MSDs
    FITTING_RANGE=[0,100]

    #tracking parameters
    MAX_DIST=80 # maximum displacement between frames in pixel
    MAX_MISSED_FRAME=10 # allowed number of frames a particle can disappear
    MIN_FRAME=10 # minimum number of frames a trajectory needs to last
    PIXEL_SIZE=1.1 # image pixel size in micron/pixel, specific for each scope and lens (Cytiva 10X: 0.65) and (Spinning Disk: 1.1 at 10X)
    MAX_LAG_TIME=160 # intervals of frames out to which MSD is computed


config = Config()
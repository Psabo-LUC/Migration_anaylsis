class Config:
    #TIFF file post processing
    FRAME_RATE = 300 #second/frames
    DOWN_SAMPLING= 0
    CROP=[[0,2000],[0,2000]]
    THRESHOLD=13900
    VIDEO_LENGTH = 25 #length - 1 for zero indexing


    #Valid cell parameters 
    DIAMETER=71
    MIN_MASS=3500000

    # for fitting MSDs
    FITTING_RANGE=[0,20]

    #tracking parameters
    MAX_DIST=100 # maximum displacement between frames in pixel
    MAX_MISSED_FRAME=1 # allowed number of frames a particle can disappear
    MIN_FRAME=10 # minimum number of frames a trajectory needs to last
    PIXEL_SIZE=0.65 # image pixel size in micron/pixel, specific for each scope and lens (Cytiva 10X: 0.65) and (Spinning Disk: 1.1 at 10X)
    MAX_LAG_TIME=300 # intervals of frames out to which MSD is computed



config = Config()
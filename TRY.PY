from Utils import read_video, save_video
import cv2
import numpy as np 
def Traingle(frame,x,y):
    triangle_points = np.array([
        [x,y],
        [x-10,y-20],
        [x+10,y-20],
    ])
    cv2.drawContours(frame, [triangle_points],0,(255,255,255), cv2.FILLED)
    cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)
    return frame
def main():
    # Read Video
    video_frames = read_video('TRY.mp4')
    print("ABC","\n")
    
    output_video_frames=[]
    for frame_num, frame in enumerate(video_frames):
        frame = frame.copy()
        frame=Traingle(frame,10,935)
        frame=Traingle(frame,365,275)
        frame=Traingle(frame,1150,260)
        frame=Traingle(frame,1900,915)
        
        output_video_frames.append(frame)   
    print("ABC","\n")
    # Save video
    save_video(output_video_frames, 'Output/TRIED.avi')

if __name__ == '__main__':
    main()
    
    
    
    #               1---->  4    &   14--->20
        # self.pixel_vertices = np.array([[110, 1035], 
        #                        [265, 275], 
        #                        [910, 260], 
        #                        [1640, 915]])
        
        
        
                    # FRAME 5---->14
    # #frame=Traingle(frame,-80,800)
    #     frame=Traingle(frame,1450,320)
    #     frame=Traingle(frame,650,305)
    #     frame=Traingle(frame,1840,900)
    
    
                #  Frame   21--->end
                
    #      frame=Traingle(frame,250,900)
    #     frame=Traingle(frame,1100,290)
    #     frame=Traingle(frame,150,340)
    #     frame=Traingle(frame,2000,650)
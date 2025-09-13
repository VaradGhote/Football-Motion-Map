import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import pickle
import sys 

sys.path.append(r"D:\TY__sem-1\EDI-2")
from Utils import read_video, save_video


def generate_graph_frame(tracks, img):
    stub_path = 'stubs/data2.pkl'
    if stub_path is not None and os.path.exists(stub_path):
        with open(stub_path, 'rb') as f:
            data2 = pickle.load(f)
    
    if not data2:
        raise ValueError("Stub file 'data2.pkl' not properly loaded.")

    output_video_frames = []
    for frame_num, track in enumerate(tracks['players']):
        print(frame_num,"\n")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(-5, 112)
        ax.set_ylim(-2, 69)
        ax.imshow(img, extent=[-5, 112, -2, 69], aspect='equal')
        
        for track_id, track_info in track.items():
            pos_trans = data2['players'][frame_num][track_id].get('position_transformed')
            if pos_trans is not None:
                x, y = pos_trans
                y= 68-y
                if 0 < frame_num < 100:
                    x += 46.7
                elif 100 <= frame_num < 350:
                    x += 23.4
                elif 350 <= frame_num < 500:
                    x += 40.84
                elif 500 <= frame_num < 800:
                    x += 52.5
                if tracks['players'][frame_num][track_id]['team'] == 1:
                    ax.plot(x, y, 'o', markersize=15, color='blue', markeredgewidth=2, markeredgecolor='black' , linestyle='None')
                if tracks['players'][frame_num][track_id]['team'] == 2:
                    ax.plot(x, y, 'o', markersize=15,  markerfacecolor='white', markeredgewidth=2, markeredgecolor='red' , linestyle='None')
            
                
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        
        fig.canvas.draw()
        frame1 = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        frame1 = frame1.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        frame1 = frame1[:, :, :3]
        
        plt.close(fig)
        output_video_frames.append(frame1)

    return output_video_frames


# Background image
background_image = "D:\TY__sem-1\EDI-2\plot_graph\Field.jpg"  # Path to your background image

# Load the background image
img = mpimg.imread(background_image)
stub_path = 'stubs/data.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path,'rb') as f:
        tracks = pickle.load(f)
print("123\n")
output_video_frames = []

output_video_frames =  generate_graph_frame(tracks,img)

    
    
save_video(output_video_frames , 'D:/TY__sem-1/EDI-2/Output/Plot2.avi')




# # Show the plot
# plt.show()

import numpy as np
import cv2
import os
import pickle
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

stub_path = 'stubs/data2.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path, 'rb') as f:
        data2 = pickle.load(f)
        
stub_path = 'stubs/data.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path,'rb') as f:
        tracks = pickle.load(f)

points =[]
for frame_num, track in enumerate(tracks['players']):
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
    points.append((x,y))   
bg_img = mpimg.imread("D:\TY__sem-1\EDI-2\plot_graph\Field.jpg")
# Extract x and y coordinates
x_coords, y_coords = zip(*points)

# Create a 2D histogram (heatmap data) using np.histogram2d
heatmap_data, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=(10, 10), range=[[0, 105], [0, 68]])
## Create the heatmap
plt.figure(figsize=(10, 6))  # Set the figure size to match the frame scale
sns.heatmap(heatmap_data.T, xticklabels=xedges, yticklabels=yedges, cmap='YlGnBu', square=False)


# Adjust aspect ratio to fit the frame
plt.gca().set_aspect('auto', adjustable='box')




# Show the plot
plt.show()
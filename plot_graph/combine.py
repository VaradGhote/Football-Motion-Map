import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import os
import sys
import matplotlib.image as mpimg

data = []
stub_path = 'stubs/data2.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path, 'rb') as f:
        data2 = pickle.load(f)

stub_path = 'stubs/IDS.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path, 'rb') as f:
        IDS = pickle.load(f)
        
stub_path = 'stubs/data.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path,'rb') as f:
        tracks = pickle.load(f)

for frame_num, track in enumerate(tracks['players']):
        # for track_id, track_info in track.items():

            if 2 not in IDS[frame_num+1][1]:  # Initialize player list if not present
                        IDS[frame_num+1][1][2] = []
            a = IDS[frame_num+1][1][1][0]
            pos_trans = data2['players'][frame_num][a].get('position_transformed')
            x=0
            y=0
            if pos_trans is not None:
                x, y = pos_trans
                y= 68-y
                if 0 <= frame_num < 100:
                    x += 46.7
                elif 100 <= frame_num < 350:
                    x += 23.4
                elif 350 <= frame_num < 500:
                    x += 40.84
                elif 500 <= frame_num < 800:
                    x += 52.5
            data.append((x,y))   

bg_img = mpimg.imread("D:\TY__sem-1\EDI-2\plot_graph\Field.jpg")



field_img = plt.imread("D:\TY__sem-1\EDI-2\plot_graph\Field.jpg")
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-5, 112)
ax.set_ylim(-2, 69)
ax.imshow(field_img, extent=[-5, 112, -2, 69], aspect='equal')  # Assuming the field's coordinate system is 0 to 100
x_coords, y_coords = zip(*data)
ax.plot(x_coords, y_coords, label=1, color='red' )

ax.set_title(f"{1} Movement")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.legend()
ax.set_xlim([-5, 112])
ax.set_ylim([-2, 69])
ax.grid(True)

plt.show()
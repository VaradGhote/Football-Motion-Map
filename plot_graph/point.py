import numpy as np
import cv2
import os
import pickle
import sys 

sys.path.append(r"D:\TY__sem-1\EDI-2")
from Utils import read_video, save_video


stub_path = 'stubs/data.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path,'rb') as f:
        tracks = pickle.load(f)

frame_dict={frame: {1: {}, 2: {}} for frame in range(1, 751)}

for frame_num, track in enumerate(tracks['players'], start=1):  # Start from frame 1
    for track_id, track_info in track.items():
        team = track_info['team']  # Get the team of the current track_id

        # Team 1 assignment
        if team == 1:
            assigned = False
            for player, track_list in frame_dict[frame_num][1].items():
                if int(track_id) in track_list:  # Cast track_id to a regular integer
    # Your code here
  # Check if track_id is already assigned
                    assigned = True
                    break
            if not assigned:
                for player in range(1, 11):  # Players 1 to 10
                    if player not in frame_dict[frame_num][1]:  # Initialize player list if not present
                        frame_dict[frame_num][1][player] = []
                    frame_dict[frame_num][1][player].append(track_id)
                    break  # Assign to the first available player

        # Team 2 assignment
        elif team == 2:
            assigned = False
            for player, track_list in frame_dict[frame_num][2].items():
                if track_id in track_list:  # Check if track_id is already assigned
                    assigned = True
                    break
            if not assigned:
                for player in range(15, 28):  # Players 15 to 27
                    if player not in frame_dict[frame_num][2]:  # Initialize player list if not present
                        frame_dict[frame_num][2][player] = []
                    frame_dict[frame_num][2][player].append(track_id)
                    break  # Assign to the first available player
        
       
        
stub_path = 'stubs/IDS.pkl'
if stub_path is not None:
    with open(stub_path,'wb') as f:
        pickle.dump(frame_dict,f)
    
    
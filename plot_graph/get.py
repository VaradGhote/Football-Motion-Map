import numpy as np
import cv2
import os
import pickle
import sys

stub_path = 'stubs/data.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path, 'rb') as f:
        tracks = pickle.load(f)

sys.path.append(r"D:\TY__sem-1\EDI-2")
from Utils import read_video, save_video


def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def get_x_y(frame_num, track_id,bbox):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        return (x_center, y2)
    


# Initialize frame_dict
frame_dict = {frame: {1: {}, 2: {}} for frame in range(1, 760)}

for frame_num, track in enumerate(tracks['players'], start=1):  # Start from frame 1
    for track_id, track_info in track.items():
        team = track_info['team']  # Get the team of the current track_id

        # Team 1 assignment
        if team == 1:
            assigned = False
            for player, track_list in frame_dict[frame_num][1].items():
                if track_id in track_list:  # Check if track_id is already assigned
                    assigned = True
                    break
            if not assigned:
                for player in range(1, 11):  # Players 1 to 10
                    if player not in frame_dict[frame_num][1]:  # Initialize player list if not present
                        frame_dict[frame_num][1][player] = []
                    bbox = track_info['bbox']
                    frame_dict[frame_num][1][player] = get_x_y(frame_num, track_id,bbox)
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
                    bbox = track_info['bbox']
                    frame_dict[frame_num][2][player] = get_x_y(frame_num, track_id,bbox)
                    break  # Assign to the first available player

    # Debug printing for teams
    print("\nTeam 1\n", frame_dict[frame_num][1], "\n")
    print("\n\nTeam 2\n")
    print(frame_dict[frame_num][2], "\n")

# Save to pickle
stub_path = 'stubs/stats.pkl'
if stub_path is not None:
    with open(stub_path, 'wb') as f:
        pickle.dump(frame_dict, f)

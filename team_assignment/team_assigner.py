from sklearn.cluster import KMeans
import numpy as np
from scipy.stats import zscore

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.colour = {}
    
    
    def get_clustering_model(self,image):
        # Reshape the image to 2D array
        image_2d = image.reshape(-1,3)

        # Preform K-means with 2 clusters
        kmeans = KMeans(n_clusters=2, init="k-means++",n_init=1)
        kmeans.fit(image_2d)

        return kmeans

    def get_player_color(self,frame,bbox):
        image = frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]

        top_half_image = image[0:int(image.shape[0]/2),:]

        # Get Clustering model
        kmeans = self.get_clustering_model(top_half_image)

        # Get the cluster labels forr each pixel
        labels = kmeans.labels_

        # Reshape the labels to the image shape
        clustered_image = labels.reshape(top_half_image.shape[0],top_half_image.shape[1])

        # Get the player cluster
        corner_clusters = [clustered_image[0,0],clustered_image[0,-1],clustered_image[-1,0],clustered_image[-1,-1]]
        non_player_cluster = max(set(corner_clusters),key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster

        player_color = kmeans.cluster_centers_[player_cluster]

    # Check if player color is in the range (0,0,0)->(60,60,60)
        if np.all(player_color >= np.array([0, 0, 0])) and np.all(player_color <= np.array([60, 60, 60])):
            self.colour[1]=player_color
            return None  # or you could return a default color, or handle as needed


        return player_color

    
    
    def assign_team_color(self,frame, player_detections):
        
        player_colors = []
        for _, player_detection in player_detections.items():
            bbox = player_detection["bbox"]
            player_color =  self.get_player_color(frame,bbox)
            if player_color is not None:
                player_colors.append(player_color)
        
        


        kmeans = KMeans(n_clusters=2, init="k-means++",n_init=10)
        kmeans.fit(player_colors)

        self.kmeans = kmeans

        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]
        self.team_colors[3] = self.colour[1]


    def get_player_team(self,frame,player_bbox,player_id):
        # if player_id in self.player_team_dict:
        #     return self.player_team_dict[player_id]

        if player_id ==123:
            team_id=1
        player_color = self.get_player_color(frame,player_bbox)
        if player_color is  None:
            return 3
        team_id = self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1

        if player_id ==123:
            team_id=1

        self.player_team_dict[player_id] = team_id

        return team_id
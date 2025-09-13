import numpy as np 
import cv2
import pickle

class ViewTransformer():
    def __init__(self):
        court_width = 68
        court_length = 23.32

        self.pixel_vertices1 = np.array([[110, 1035], [265, 275], [910, 260], [1640, 915]])  #0
        self.pixel_vertices2 = np.array([[-80, 800],[650, 305], [1450, 320],  [1840, 900]])  #7
        self.pixel_vertices3 = np.array([[10, 935], [365, 275], [1150, 260], [1900, 915]])   #17
        self.pixel_vertices4 = np.array([[250, 900],  [150, 340],[1100, 290], [2000, 650]])  #24
        
        
        
        self.target_vertices1 = np.array([[0,court_width],[0, 0],[23.33, 0],[23.33, court_width]])
        self.target_vertices2 = np.array([[0,court_width],[0, 0],[40.84, 0],[40.84, court_width]])
        self.target_vertices3 = np.array([[0,court_width],[0, 0],[29.17, 0],[29.17, court_width]])
        self.target_vertices4 = np.array([[0,court_width],[0, 0],[52.5, 0],[52.5, court_width]])

        self.pixel_vertices1 = self.pixel_vertices1.astype(np.float32)
        self.pixel_vertices2 = self.pixel_vertices2.astype(np.float32)
        self.pixel_vertices3 = self.pixel_vertices4.astype(np.float32)
        self.pixel_vertices4 = self.pixel_vertices3.astype(np.float32)
        self.target_vertices1 = self.target_vertices1.astype(np.float32)
        self.target_vertices2 = self.target_vertices2.astype(np.float32)
        self.target_vertices3 = self.target_vertices3.astype(np.float32)
        self.target_vertices4 = self.target_vertices4.astype(np.float32)
        


    def transform_point(self,point,persepctive_trasnformer,vertex):
        p = (int(point[0]),int(point[1]))
        is_inside = cv2.pointPolygonTest(vertex,p,False) >= 0 
        if not is_inside:
            return None

        reshaped_point = point.reshape(-1,1,2).astype(np.float32)
        tranform_point = cv2.perspectiveTransform(reshaped_point,persepctive_trasnformer)
        return tranform_point.reshape(-1,2)

    def add_transformed_position_to_tracks(self,tracks):
        
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info['position_adjusted']
                    position = np.array(position)
                    vertex=self.pixel_vertices1
                    persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices1, self.target_vertices1)
                    if frame_num > 0 and frame_num < 100:
                        vertex=self.pixel_vertices1
                        persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices1, self.target_vertices1) 
                    if frame_num > 100 and frame_num < 350:
                        vertex=self.pixel_vertices2
                        persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices2, self.target_vertices2) 
                    if frame_num > 350 and frame_num < 500:
                        vertex=self.pixel_vertices3
                        persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices3, self.target_vertices3) 
                    if frame_num > 500 and frame_num < 800:
                        vertex=self.pixel_vertices4
                        persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices4, self.target_vertices4) 
                    
                    position_trasnformed = self.transform_point(position,persepctive_trasnformer,vertex)
                    if position_trasnformed is not None:
                        position_trasnformed = position_trasnformed.squeeze().tolist()
                    tracks[object][frame_num][track_id]['position_transformed'] = position_trasnformed
        
        stub_path = 'stubs/data2.pkl'
        if stub_path is not None:
            with open(stub_path,'wb') as f:
                pickle.dump(tracks,f)
        
def get_object_tracks(self,frames,read_from_stub = False , stub_path=None):
        
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path,'rb') as f:
                tracks = pickle.load(f)
            return tracks
        
        detections=self.detect_frames(frames)
        
        tracks={
            "players":[],
            "referees":[],
            "ball":[]
        }
        
        for frame_num , detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v:k for k,v in cls_names.items()}
            print(cls_names)
           
           #XYXY format
            detection_supervision = sv.Detections.from_ultralytics(detection)
            
            #GK->player
            for object_ind , class_id in enumerate(detection_supervision.class_id):
                if cls_names[class_id] == "goalkeeper":
                    detection_supervision.class_id[object_ind]=cls_names_inv["player"]
            #Tracking
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)
           
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})
            
            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id =frame_detection[3]
                track_id = frame_detection[4]
                
                print(frame_num)
                print("hello")

                if cls_id == cls_names_inv["player"]:
                        tracks["players"][frame_num][track_id]={"bbox":bbox}
                if cls_id == cls_names_inv["referee"]:
                        tracks["referees"][frame_num][track_id]={"bbox":bbox}
           
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                if cls_id == cls_names_inv['ball']:
                    tracks["ball"][frame_num][1] = {"bbox":bbox}
        
        if stub_path is not None:
            with open(stub_path,'wb') as f:
                pickle.dump(tracks,f)
           
        return tracks
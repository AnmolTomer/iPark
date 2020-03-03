import yaml
import numpy as np
import cv2

class car_detect():
    """
    Constructor for Class: car_detect
        Input:
            video_path => type int for camera or string for file_path
            slot_yaml => path to yml file for the defined slots
            classifier_path => path to classifier for the detection
    """
    def __init__(self,video_path):#,slot_yaml,classifier_path):
        """
        Constructor for Class: car_detect
        Input:
            video_path => type int for camera or string for file_path
            slot_yaml => path to yml file for the defined slots
            classifier_path => path to classifier for the detection
        """
        self.video_path = "//home//rahul//Programming//Hackathons//Skillenza//Videos//vid1.mp4"
        self.slot_yaml = "//home//rahul//Programming//Hackathons//Skillenza//Vatican//Utilities//bera_yml.yml"
        cascade_src = '//home//rahul//Programming//Hackathons//Skillenza//Vatican//Utilities//Khare_classifier_02.xml'
        self.car_cascade = cv2.CascadeClassifier(cascade_src)
        self.is_car_present = False
        self.global_str = "Last change at: "
        self.change_pos = 0.00
        self.dict =  {
            'text_overlay': False,
            'parking_overlay': True,
            'parking_id_overlay': True,
            'parking_detection': True,
            'min_area_motion_contour': 500, # area given to detect motion
            'park_laplacian_th': 2.8, 
            'park_sec_to_wait': 1, # 4   wait time for changing the status of a region
            'start_frame': 0, # begin frame from specific frame number 
            'show_ids': True, # shows id on each region
            'classifier_used': True,
        }
        # Set from video
        self.cap = cv2.VideoCapture(self.video_path)
        # Read YAML data (parking space polygons)
        with open(self.slot_yaml, 'r') as stream:
            self.parking_data = yaml.full_load(stream)
        # Variables for Parking data
        self.parking_contours = []
        self.parking_bounding_rects = []
        self.parking_mask = []
        self.parking_slots_busy = []
        # Create a mask, if the user has already defined the slots
        if self.parking_data != None:
            for park in self.parking_data:
                points = np.array(park['points'])
                rect = cv2.boundingRect(points)
                points_shifted = points.copy()
                points_shifted[:,0] = points[:,0] - rect[0] # shift contour to region of interest
                points_shifted[:,1] = points[:,1] - rect[1]
                self.parking_contours.append(points)
                self.parking_bounding_rects.append(rect)
                mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                            color=255, thickness=-1, lineType=cv2.LINE_8)
                self.mask = mask==255
                self.parking_mask.append(mask)
        
        if self.parking_data != None:
            self.parking_status = [False]*len(self.parking_data)
            self.parking_slots_busy = [False]*len(self.parking_data)
            self.parking_buffer = [None]*len(self.parking_data)
        
        print("Variables set! Object Initialized and Ready to go!")

        # while(True):
        #     cv2.imshow("Test __init__",self.cap.read()[1])
        #     if(cv2.waitKey(1)==ord('q')):
        #         break
         
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    # Print parkIDs in the feed
    def print_parkIDs(self,park, coor_points, frame_rev):
        """
        Print Parking IDs on the image
        """
        moments = cv2.moments(coor_points)
        centroid = (int(moments['m10']/moments['m00'])-3, int(moments['m01']/moments['m00'])+3)
        # putting numbers on marked regions
        cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

    # Check if the image has a car
    def run_classifier(self, img, id):
        """The Classifier"""
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cars = self.car_cascade.detectMultiScale(img, 1.1, 1)
        if cars == ():
            return False
        else:
            # parking_status[id] = False
            return True
    
    def slots_with_car(self):
        """Return a list of boolean values representing the slot being busy or available"""
        while(True):
            if(not self.cap.isOpened()):
                return None
            video_cur_pos = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Current position of the video file in seconds
            video_cur_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES) # Index of the frame to be decoded/captured next
            ret, frame_initial = self.cap.read()
            if ret == True:
                frame = cv2.resize(frame_initial,(720,720))
                cv2.imshow("Test",frame_initial)
            if ret == False:
                print("Video ended")
                return None

            # Background Subtraction
            frame_blur = cv2.GaussianBlur(frame.copy(), (5,5), 3)
            frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
            frame_out = frame.copy()

            # detecting cars and vacant spaces
            if self.dict['parking_detection']:
                for ind, park in enumerate(self.parking_data):
                    points = np.array(park['points'])
                    rect = self.parking_bounding_rects[ind]
                    roi_gray = frame_gray[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] # crop roi for faster calcluation
                    roi_laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
                    points[:,0] = points[:,0] - rect[0] # shift contour to roi
                    points[:,1] = points[:,1] - rect[1]
                    delta = np.mean(np.abs(roi_laplacian * self.parking_mask[ind]))
                    # if(delta<2.5):
                        # print("ind, del", ind, delta)
                    status = delta < self.dict['park_laplacian_th']
                    # If detected a change in parking status, save the current time
                    if status != self.parking_status[ind] and self.parking_buffer[ind]==None:
                        self.parking_buffer[ind] = video_cur_pos
                        self.change_pos = video_cur_pos
                    # If status is still different than the one saved and counter is open
                    elif status != self.parking_status[ind] and self.parking_buffer[ind]!=None:
                        if video_cur_pos - self.parking_buffer[ind] > self.dict['park_sec_to_wait']:
                            self.parking_status[ind] = status
                            self.parking_buffer[ind] = None
                    # If status is still same and counter is open
                    elif status == self.parking_status[ind] and self.parking_buffer[ind]!=None:
                        self.parking_buffer[ind] = None

            # changing the color on the basis on status change occured in the above section and putting numbers on areas
            if self.dict['parking_overlay']:
                self.parking_slots_busy = [False]*len(self.parking_data)
                print("Reset the list:",self.parking_slots_busy)
                for ind, park in enumerate(self.parking_data):
                    points = np.array(park['points'])
                    self.is_car_present = False
                    if self.parking_status[ind]:
                        color = (0,255,0)
                        self.is_car_present = False
                        rect = self.parking_bounding_rects[ind]
                        roi_gray_ov = frame_gray[rect[1]:(rect[1] + rect[3]),
                                    rect[0]:(rect[0] + rect[2])]  # crop roi for faster calcluation
                        res = self.run_classifier(roi_gray_ov, ind)
                        if res:
                            # del parking_data[ind]
                            color = (0,0,255)
                            self.is_car_present = True
                    else:
                        color = (0,0,255)
                        self.is_car_present = True
                    # print(park, str(ind), self.is_car_present)
                    self.parking_slots_busy[ind] = self.is_car_present
                    cv2.drawContours(frame_out, [points], contourIdx=-1,
                                        color=color, thickness=2, lineType=cv2.LINE_8)
                    if self.dict['show_ids']:
                            self.print_parkIDs(park, points, frame_out)
                print("Detected Final list:",self.parking_slots_busy)
                cv2.imshow('frame', frame_out)
                # return self.parking_slots_busy
            # return None
        
        




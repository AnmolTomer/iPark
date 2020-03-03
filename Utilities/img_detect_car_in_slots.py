import yaml
import numpy as np
import cv2

import argparse
parser = argparse.ArgumentParser(description='Detect Cars in Image')
parser.add_argument('file', metavar='FILE', help='file path to run detection on')
parser.add_argument('fyaml', metavar='FILE', help='file path of yml')
args = parser.parse_args()

# path references
fn = args.file
fn_yaml = args.fyaml
cascade_src = '//home//rahul//Programming//Hackathons//Skillenza//Vatican//Utilities//Khare_classifier_02.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)
global_str = "Last change at: "
change_pos = 0.00
dict =  {
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

def run_classifier(img, id):
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(img, 1.1, 1)
    if cars == ():
        return False
    else:
        # parking_status[id] = False
        return True

# Read YAML data (parking space polygons)
with open(fn_yaml, 'r') as stream:
    parking_data = yaml.full_load(stream)
parking_contours = []
parking_bounding_rects = []
parking_mask = []
if parking_data != None:
    for park in parking_data:
        points = np.array(park['points'])
        rect = cv2.boundingRect(points)
        points_shifted = points.copy()
        points_shifted[:,0] = points[:,0] - rect[0] # shift contour to region of interest
        points_shifted[:,1] = points[:,1] - rect[1]
        parking_contours.append(points)
        parking_bounding_rects.append(rect)
        mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                    color=255, thickness=-1, lineType=cv2.LINE_8)
        mask = mask==255
        parking_mask.append(mask)

kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) # morphological kernel
kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,(5,19))
if parking_data != None:
    parking_status = [False]*len(parking_data)
    parking_buffer = [None]*len(parking_data)
# bw = ()
def print_parkIDs(park, coor_points, frame_rev):
    moments = cv2.moments(coor_points)
    centroid = (int(moments['m10']/moments['m00'])-3, int(moments['m01']/moments['m00'])+3)
    # putting numbers on marked regions
    cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(frame_rev, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
while(True):
    frame_initial = cv2.imread(args.file)
    frame = cv2.resize(frame_initial,(720,720))

    # Background Subtraction
    frame_blur = cv2.GaussianBlur(frame.copy(), (5,5), 3)
    # frame_blur = frame_blur[150:1000, 100:1800]
    frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
    frame_out = frame.copy()

    # detecting cars and vacant spaces
    if dict['parking_detection']:
        for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            rect = parking_bounding_rects[ind]
            roi_gray = frame_gray[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] # crop roi for faster calcluation

            roi_laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
            points[:,0] = points[:,0] - rect[0] # shift contour to roi
            points[:,1] = points[:,1] - rect[1]
            delta = np.mean(np.abs(roi_laplacian * parking_mask[ind]))
            status = delta < dict['park_laplacian_th']
            # If detected a change in parking status, save the current time
            if status != parking_status[ind] and parking_buffer[ind]==None:
                # parking_buffer[ind] = video_cur_pos
                # change_pos = video_cur_pos
                pass
            # If status is still different than the one saved and counter is open
            elif status != parking_status[ind] and parking_buffer[ind]!=None:
                # if video_cur_pos - parking_buffer[ind] > dict['park_sec_to_wait']:
                parking_status[ind] = status
                    # parking_buffer[ind] = None
            # If status is still same and counter is open
            elif status == parking_status[ind] and parking_buffer[ind]!=None:
                parking_buffer[ind] = None

    # changing the color on the basis on status change occured in the above section and putting numbers on areas
    if dict['parking_overlay']:
        res1 = False
        parking_slots_busy = parking_status.copy()
        for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            if parking_status[ind]:
                color = (0,255,0)
                res1 = False
                rect = parking_bounding_rects[ind]
                roi_gray_ov = frame_gray[rect[1]:(rect[1] + rect[3]),
                               rect[0]:(rect[0] + rect[2])]  # crop roi for faster calcluation
                res = run_classifier(roi_gray_ov, ind)
                if res:
                    # del parking_data[ind]
                    color = (0,0,255)
                    res1 = True
            else:
                color = (0,0,255)
                res1 = True
            parking_slots_busy[ind] = res1
            cv2.drawContours(frame_out, [points], contourIdx=-1,
                                 color=color, thickness=2, lineType=cv2.LINE_8)
            if dict['show_ids']:
                    print_parkIDs(park, points, frame_out)
        print(parking_slots_busy)
            

    # Display video
    cv2.imshow('frame', frame_out)
    # cv2.imshow('background mask', bw)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if cv2.waitKey(33) == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()   
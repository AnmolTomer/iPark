def get_image():
    import cv2 
    import time
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    store = int(time.time())
    a = store

    while True:
        try:
            check, frame = webcam.read()
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'): 
                cv2.imwrite(filename=(f'app/img/{store}.jpg'), img=frame)
                webcam.release()

            # img_new = cv2.imread((f'{store}.jpg'), cv2.IMREAD_GRAYSCALE)
            # img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                # b = print(f"{store}.jpg")
                
                # print("Processing image...")
                # print("Image saved!")

        
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
    return(f"{store}.jpg")

# a = get_image()
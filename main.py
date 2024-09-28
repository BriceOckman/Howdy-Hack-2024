
import cv2
import time

def detect_faces_eyes_from_frame(frame, draw=False):
    
    '''
    input:
        frame: image
    output:
        int, number of faces detected
    '''
    
    # return variable
    count = 0

    # Load Haar cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    # Read an image or video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop over detected faces
    for (x, y, w, h) in faces:

        if draw: cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Focus on the face region
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Check if two eyes are detected
        if len(eyes) == 2:

            if draw:
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            count += 1  # increase count for a successful face+2eyes detection
    
    return count, frame

def get_retention(filename, folder=None, step_through=False, debug=False):
    
    '''
    input:
        filename: string of video file, name + extension
        folder: string of folder name.
                when set, individual marked frames will be saved here.
        step_through: boolean. when set, cv2 will open a marked image
                      preview window.
        debug: boolean. when set, retention values will be printed as
               well as returned.

    output:
        [int, int, int, ...] list of retention values

    '''
    cap = cv2.VideoCapture(filename)
    count = 0
    retention_values = []

    status, frame = cap.read()
    while status:
        # if user requested to save all frames to folder
        if folder: cv2.imwrite(os.path.join(folder, "frame%d.jpg" % count), frame)

        # the meat
        retention, marked_frame = detect_faces_eyes_from_frame(frame, draw=(folder != None or step_through))
        retention_values.append(retention)
     
        # if we're in step_through mode
        if step_through:   
            cv2.imshow('frame-by-frame viewer: press n', marked_frame)
            print(f'Frame Count: {count}, Retention: {retention}')
            while cv2.waitKey(10) & 0xFF != ord('n'):
                pass 
                
        count = count + 1
        status, frame = cap.read()
    
    # if image previews were opened (only possible in step_through mode) 
    if step_through:
        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows
    
    if debug:
        for i in retention_values:
            print(i, end=', ')

    return retention_values

get_retention('test_video.mp4')

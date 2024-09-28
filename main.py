
import cv2
import time

def detect_faces_eyes_from_frame(frame):
    
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
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Focus on the face region
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Check if two eyes are detected
        if len(eyes) == 2:
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            count += 1  # increase count for a successful face+2eyes detection
    
    cv2.imwrite(f'{time.time()}.jpg', frame)
    return count

def get_frames(filename):
    
    '''
    input:
        filename: video filename
    output:
        [Image?, ...] list of Image objects (image class unknown)
    '''
    
    video = cv2.videocapture(filename)
    success, image = video.read()  # read initial frame
    while success:  # while frame reading is successful
        yield image
        success, image = video.read() 

def detect_faces(filename):
    
    '''
    input:
        filename: video filename
    output:
        [int, int, ...] list of faces detected/frame
    '''
    
    return [detect_faces_eyes_from_frame(frame) in get_frames(filename)]

def main(i):
    img = cv2.imread(f'{i}.jpg')
    print(detect_faces_eyes_from_frame(img))

main('test_two')
main('test_one')
main('test_zero')

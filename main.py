
# ppt
import re
# import xml.etree.ElementTree as ET
import zipfile
import os

import cv2
import shutil

# for fuzzy search
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from collections import Counter

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

def clean_up(folderpath):
    shutil.rmtree(folderpath)

def get_text(filename, debug=False):
        
    '''
    input:
        filename: string of powerpoint

    output:
        [str, str, ...] - list of strings representing a list
                          of text from each slide
    '''
    
    if '.pptx' not in filename:
        raise Exception("Invalid filetype .{filename.split('.')[-1]} supported. Only .pptx please!")
    # return variable
    slide_script = []

    try:
        # assuming user inputted a pptx
        filepath = os.path.join(os.getcwd(), filename)
        shutil.copy(filepath, filepath+'.zip')

        # make folder by taking filename (split/cut off file extension)
        folder = os.path.basename(filepath).split('.')[0]

        # if folder exists, delete it
        if os.path.exists(folder): shutil.rmtree(folder)

        # os.makedirs(folder)
        folderpath = os.path.join(os.getcwd(), folder)
        
        # extract files
        with zipfile.ZipFile(os.path.join(os.getcwd(), filepath+'.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

        slidespath = os.path.join(folderpath, 'slides')
        filenames = [file for file in os.listdir(slidespath) if '.' in file and 'xml' in file]
        sorted_filenames = sorted(filenames, key=lambda f: int(re.search(r'\d+', f).group()))
        
        for file in sorted_filenames:
            with open(os.path.join(slidespath, file), 'r') as f:
                content = f.read()
            pattern = r'<a:t>(.*?)</a:t>'
            matches = re.findall(pattern, content)
            slide_script.append(matches)
            if debug: print(f'{file = } {len(matches) = }')
        
            # i believe that only xml files can exist here
            # this is an warning
            if 'xml' not in file and debug:
                print(f'WARNING: non-xml file found: {file}')
        
        return slide_script

    except Exception as e:
        raise e

    finally:
        clean_up(folderpath)

get_text('test_ppt.pptx')

def find_unique(slide_text_list):
    '''
    parses through slide_text_list and finds unique words on each slide
    '''
    unique_words_sorted = []
    slide_words = "".join(slide_text_list)
    words = re.findall(r'\b\w+\b', slide_words.lower())
    word_counts = (Counter(words))
    
    for line in slide_text_list:
        temp_list = []
        line_list = line.split(' ')
        for word in line_list:
            if 1 == word_counts[word] or word_counts[word] == line_list.count(word):
                temp_list.append(word)
            
        unique_words_sorted.append(temp_list)

def fuzzy_search(slide_text_list, transcript_text):
    '''
    
    '''
    pass

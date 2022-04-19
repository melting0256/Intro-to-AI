import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    First,we use readline to read the filename of image and split the filename and the 
    amount of faces.Second,we read and split each x,y,height,and wide of each faces,then
    we crop the arange of faces and turn them into grayscale and 19x19.Finally,we use 
    clf.classify to determine whether the image is face or not.If we get 1,that means 
    the image is face,it will have a green frame.If we get 0,it will have a red frame.
    """
    file=open(dataPath)
    for j in range(2):
        line=file.readline()
        line=line.split()
        img=cv2.imread(os.path.join(r"data\detect",line[0]))
        #print("img:",img)
        for i in range(int(line[1])):
            position=file.readline()
            position=position.split()
            green_color=(0,255,0)
            red_color=(0,0,255)
            x=int(position[0])
            y=int(position[1])
            w=int(position[2])
            h=int(position[3])
            crop_img=img[y:y+h,x:x+w]
            image=cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
            cv2.waitKey(0)
            image=cv2.resize(image,(19,19))
            if clf.classify(image)==1:
                cv2.rectangle(img,(x,y),(x+w,y+h),green_color,2)
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),red_color,2)
        cv2.imshow("final",img)
        cv2.waitKey(0)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)

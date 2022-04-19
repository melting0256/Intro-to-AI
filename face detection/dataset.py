import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
    use for loop to load all folders in test and train,then use os.join.path 
    to generate the new path for the images.Determine whether the image is from 
    the folder named 'face'.If the image is from 'face',it will be stored with 
    the form image=(image,1).In contrast, if the image is from 'non-face',it
    will be stored with the form img=(img,0).All images will be appended in 
    dataset.
    """
    dataset=[]
    for filename in os.listdir(dataPath):
        result1=os.path.join(dataPath,filename)
        if filename == 'face':
            for i in os.listdir(result1):
                result2=os.path.join(result1,i)
                img=cv2.imread(result2,cv2.IMREAD_GRAYSCALE)
                img=(img,1)
                dataset.append(img)
        if filename == 'non-face':
            for i in os.listdir(result1):
                result2=os.path.join(result1,i)
                img=cv2.imread(result2,cv2.IMREAD_GRAYSCALE)
                img=(img,0)
                dataset.append(img)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    return dataset
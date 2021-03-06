import numpy as np
import cv2
import os

def listdir(path, list_name):  #Read folder
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)

def load_img(list_name,img_list): #Read images
    for i in list_name:
        img_list.append(cv2.imread(i))


def save_img(list_name, img_list):  #Write images
    j=0
    for i in list_name:
        new_path = 'calibresult1/n_' + i[5:]
        cv2.imwrite(new_path,img_list[j])
        j = j + 1

def undistort(img,k):
    #Basic setting and parameters acquisition
    parameters = np.load("parameters1.npz")
    mtx = parameters["mtx"]
    dist = parameters["dist"]
    rvecs = parameters["rvecs"]
    tvecs = parameters["tvecs"]

    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    #undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    ##crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    #re-projection error
    mean_error = 0

    points = np.load("points1.npz")
    objpoints = points["objpoints"]
    imgpoints = points["imgpoints"]
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist) #transform the object point to image point
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    #error print
    if k<=8:
        print ('total error of image',k+1,':',mean_error/len(objpoints))
    else:
        print ('total error of image',k+2,':',mean_error/len(objpoints))
    return dst

if __name__ == '__main__':
    path='im_1'
    l=[] #store images' path
    i=[] #store images
    listdir(path,l)
    load_img(l,i)

    for k in range(0,len(i)):
        i[k]=undistort(i[k],k)

    save_img(l,i)

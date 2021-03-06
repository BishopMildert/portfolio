# necessary packages
import numpy as np
import cv2


def order_points(pts):
    
    ''' 
    A list of coordinates that will be ordered so that the index order
    is as follow:

    1st item = top-left;
    2nd item = top-right;
    3rd item = bottom-right'
    4th item = bottom-left

    '''

    rect = np.zeros((4,2), dtype='float32')

    # top-left point will have the smallest sum,
    # whereas bottom-right will have the largest
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # computing the difference between the points
    # top-right will have the smallest difference,
    # whereas bottom-left will have the largest
    diff= np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # returning the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be 
    # the  maximum distance between bottom-right and bottom-left
    # x-coordinates or the top-right and top left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # the height of the new image - the maximum distance between
    # the top-right and bottom-right - y-coordinates or top-left
    # and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2 )+ ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))


    dst = np.array([
        [0, 0],
        [maxWidth -1, 0],
        [maxWidth -1 , maxHeight -1],
        [0, maxHeight - 1]], dtype='float32')

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped
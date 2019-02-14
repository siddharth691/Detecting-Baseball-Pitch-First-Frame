#Detecting the release frame for the pitcher in a baseball game


Requirements:
--------------
1. OpenCV
2. Numpy
3. Argparse

Usage:
------
python detect_release_frame.py --path [PATH] --thresh [THRESH] --mask_coord [MASK COORDINATES IN STRING]


Assumptions:
------------
1. Relative position of the pitcher with respect to camera is unchanged.


Tunable parameters:
-------------------
1. Mask where ball release can be assumed (default values : "[(390, 200), (525, 290)]")
2. threshold for segmentation (95)

Approach:
---------
I have used background separation approach to get the approximate frame number when pitcher releases the ball.

Here are the steps:
1. Resizing the input frame
2. Masking the frame around the approximate region where we can expect the release of the ball.
3. Filtering the image to remove high frequency component
4. Subtracting the consecutive frames to get only the foreground and remove background
5. Converting to grayscale
6. Thresholding to remove unwanted other pixels.
7. Now in the resulting image check if there is any white pixel, if there's any the current frame is the release frame


Further improvements:
---------------------
1. Pitcher's physical height can be incorporated while tuning the mask parameters
2. Opencv blob detection can be used to detect blob and then after morphological operations removing any blobs which are greater than approximate ball pixel size.


Results from given test videos:
-------------------------------
test2.mp4 (781)
test3.mp4 (397)
test4.mp4 (593)
test5.mp4 (593)


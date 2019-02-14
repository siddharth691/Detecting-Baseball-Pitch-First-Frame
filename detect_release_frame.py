import argparse
import cv2
import numpy as np

def operations_on_frame(prev_frame, next_frame, mask_coord, thresh= 95):
	
	"""
	Util function to perform operations on a frame
	Input:
	------
	previous frame: previous frame (in BGR)
	next frame: next frame (in BGR)
	mask_coord: (list of two tuples) upper left and lower right coordinate of the mask for the ball release region
	thresh: (int) threshold for segmenting

	Output:
	-------
	ball_mask: binary cropped mask 

	"""

	#Resizing
	p_im = cv2.resize(prev_frame, dsize = (0,0), fx = 0.3, fy = 0.3, interpolation = cv2.INTER_LINEAR)
	n_im = cv2.resize(next_frame, dsize = (0,0), fx = 0.3, fy = 0.3, interpolation = cv2.INTER_LINEAR)
	
	#Cropping for required region
	p_im = p_im[mask_coord[0][1]: mask_coord[1][1], mask_coord[0][0]: mask_coord[1][0]]
	n_im = n_im[mask_coord[0][1]: mask_coord[1][1], mask_coord[0][0]: mask_coord[1][0]]
	

	#Blurring to remove noise and high frequency component
	try:

		p_im =cv2.blur(p_im,(5,5))

	except:
		print(p_im.shape)
	n_im =cv2.blur(n_im,(5,5))
	
	#subtracting consecutive frames to get the background
	d_im = cv2.subtract(n_im,p_im)

	#Converting to grayscale
	gray_im = cv2.cvtColor(d_im, cv2.COLOR_BGR2GRAY)
		
	#Converting to binary region
	im_bw = cv2.threshold(gray_im, thresh, 255, cv2.THRESH_BINARY)
	
	#Erosion followed by (dilation x 3)
	ball_mask = cv2.erode(im_bw[1], None, iterations=1)
	ball_mask = cv2.dilate(ball_mask, None, iterations=3)
	
	return ball_mask


def detect_frame_no(video_path, mask_coord, thresh):
	
	"""
	Function that detect release frame no.

	Inputs:
	-------
	video_path: (string) path to the input video
	mask_coord: (list of two tuples) upper left and lower right coordinate of the mask for the ball release region
	thresh: (int) threshold for segmenting

	Outputs:
	--------
	found: (bool) if the release frame is found or not
	release_frame_no: (int) if the found == True -> release frame no. else -1

	"""
	cap = cv2.VideoCapture(video_path)

	f_c = 1
	found = False
	release_frame_no = -1
	ret, prev_frame = cap.read()


	while cap.isOpened():
		ret,next_frame = cap.read()
		f_c+=1

		if ret:
			next_im = operations_on_frame(prev_frame.copy(), next_frame.copy(), mask_coord, thresh = thresh)
			if(np.count_nonzero(next_im) != 0):
				
				found = True
				release_frame_no = f_c
				break
			
			prev_frame = next_frame.copy()
		
		else:
			break


	cap.release()

	return found, release_frame_no



def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("--path", default="./test1.mp4", help="path to the input video")
	parser.add_argument("--thresh", default=95, help="threshold for binary segmentation", type = int)
	parser.add_argument("--mask_coord", default="[(390, 200), (525, 290)]", help="string for list of mask coordinates (see default values)")

	args = parser.parse_args()
	arguments = args.__dict__

	#Make a dictionary of all arguments
	args_dict = {k: v for k,v in arguments.items()}

	path = args_dict['path']
	thresh = args_dict['thresh']
	st_coord = args_dict['mask_coord']

	a = st_coord.strip("[(").strip(")]").split(",")
	coord = [int(c.strip(" ").strip(')').strip('(')) for c in a]
	mask_coord = [(coord[0], coord[1]), (coord[2], coord[3])]


	found, frame_no = detect_frame_no(path, mask_coord, thresh)

	if(found == True):
		print("Found!")
		print("Frame no: {}".format(frame_no))
	else:
		print("Not found!")

if __name__ == '__main__':

	main()
	
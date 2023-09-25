import argparse
import os
import cv2
import math
import numpy as np

from tqdm import tqdm

# parser function
def make_parser():
    parser = argparse.ArgumentParser("Video to image generator!")
    parser.add_argument("--path", default="./assets/dog.jpg",  help="path  source to images or video")
    parser.add_argument("--sec",  default=5, help="desired seconds interval of each image captured")


    return parser

# main program
def main(args):

    source = args.path # will take the path specified from argparser

    os.makedirs("result", exist_ok=True) # create directory to store result, if exist skip

    path_out = "result/" # result will be save to result directory

    target_sec = int(args.sec) # will take target interval as specified from argparser

    result_counter = 0 # count how many image is saved

    frame_counter = 0 # frame counter

    frames = [] # list to store all the image in the desired interval
    
    cap = cv2.VideoCapture(source) # start opencv with source as input

    progress = cap.get(cv2.CAP_PROP_FRAME_COUNT) # number of total frame in the video

    pbar = tqdm(total = progress) # progress bar, will increment each frame

    print("Starting!")
    
    while (cap.isOpened()):

        frame_counter+=1 # increment frame counter with each iteration

        pbar.update(1) # increment progress bar

        success, frame = cap.read() # read the current frame to be used

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # timestamp of current frame

        if math.floor(float(timestamp) % target_sec) == 0: # if timestamp is the increment of interval, store frame
            frames.append(frame)
            continue

        if math.floor(int(timestamp) % target_sec) > 0: # if timestamp is not the increment of itnerval anymore, save frame as image from stored frames
            if len(frames) != 0:
                cv2.imwrite( path_out + "image%d.jpg" % result_counter, frames[0])
                print(f'saving image {result_counter} success! (frame: {frame_counter} | video timestamp: {np.round(timestamp, 2)})')
                result_countercounter+=1
                frames = []

        if frame_counter == progress: # if frame counter reach the end, finish program
            print("Completed!")
            break

    cap.release()
    
# to run the program
if __name__ == "__main__":
    args = make_parser().parse_args()
    main(args)
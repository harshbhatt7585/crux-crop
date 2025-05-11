import argparse
from multiprocessing import Pool
from crop import process_segment
from config import DEFAULT_PARAMS
import cv2
import os

def main():
    parser = argparse.ArgumentParser(
        prog="crux-crop",
        description="Smart portrait cropping from input videos"
    )
    parser.add_argument(
        "video_path",
        help="input video file"
    )
    parser.add_argument(
        "output_path",
        help="final output file"
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=None,
        help=f"override FPS (default: source footage FPS)"
    )
    parser.add_argument(
        "--crop-width",
        type=int,
        default=None,
        help=f"override crop width (default: auto-computed)"
    )
    parser.add_argument(
        "--crop-height",
        type=int,
        default=None,
        help=f"override crop height (default: auto-computed)"
    )
    parser.add_argument(
        "--cascade-path",
        default="haarcascade_frontalface_default.xml",
        help="path to Haar cascade XML"
    )
    parser.add_argument(
        "--smooth-frames",
        type=int,
        default=DEFAULT_PARAMS['smooth_frames'],
        help=f"number of frames for smoothing window (default: {DEFAULT_PARAMS['smooth_frames']})"
    )
    parser.add_argument(
        "--expansion-factor",
        type=float,
        default=DEFAULT_PARAMS['expansion_factor'],
        help=f"how much to expand the detected face box (default: {DEFAULT_PARAMS['expansion_factor']})"
    )
    parser.add_argument(
        "--scale-factor",
        type=float,
        default=DEFAULT_PARAMS['scale_factor'],
        help=f"downscale factor for face detection speed (default: {DEFAULT_PARAMS['scale_factor']})"
    )
    parser.add_argument(
        "--output_width",
        type=str,
        default=1080,
        help="width of output video"
    )
    parser.add_argument(
        "--output_height",
        type=str,
        default=1920,
        help="height of output video"
    )
    parser.add_argument(
        "--segment_duration",
        type=float,
        default=30,
        help="Cropping segment the video to process parallely, this arg can control the each segment duration"
    )

    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video_path)
    fps = args.fps or cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w,h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    params = {}
    params.update(vars(args))
    params.update({'fps': fps, 'width': w, 'height': h})
    print("Params:", params)
    desired_ar = h and w and (9/16)
    params['crop_width'] = int(h*desired_ar)
    params['crop_height'] = int(w/desired_ar)

    seg_frames = int(params['segment_duration']*fps)
    num = (total+seg_frames-1)//seg_frames
    tasks=[]
    for i in range(num):
        start = i*seg_frames
        end = min((i+1)*seg_frames, total)
        name = f"seg_{i:03d}.mp4"
        tasks.append((args.video_path, start, end, name, params))

    print(tasks)

    with Pool() as p:
        p.map(process_segment, tasks)

    with open('list.txt','w') as f:
        for _,_,_,n,_ in tasks: f.write(f"file '{n}'\n")
    os.system(f"ffmpeg -f concat -safe 0 -i list.txt -c copy {args.output_path}")
    os.remove('list.txt')



if __name__ == "__main__":
    main()

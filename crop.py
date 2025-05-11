import cv2
import numpy as np
from utils import load_face_cascade, letterbox, detect_largest_face

def process_segment(task):
    video_path, start, end, out_path, params = task
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_path, fourcc, params['fps'],
                             (params['output_width'], params['output_height']))
    cascade = load_face_cascade(params['cascade_path'])
    # init smoothing
    center_x = (params['width'] - params['crop_width'])/2
    history = [center_x]*params['smooth_frames']

    idx = start
    while idx < end:
        ret, frame = cap.read()
        if not ret: break
        faces = detect_largest_face(frame, cascade, params['scale_factor'])
        if faces:
            x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
            ew, eh = w*params['expansion_factor'], h*params['expansion_factor']
            ex = max(0, x - (ew-w)/2)
            cx = ex + ew/2
            raw = cx - params['crop_width']/2
            x_crop = np.clip(raw, 0, params['width']-params['crop_width'])
            history.append(x_crop)
            if len(history)>params['smooth_frames']: history.pop(0)
            avg = sum(history)/len(history)
            frame_cropped = frame[:, int(avg):int(avg+params['crop_width'])]
            out = cv2.resize(frame_cropped,
                             (params['output_width'], params['output_height']),
                             interpolation=cv2.INTER_AREA)
        else:
            out = letterbox(frame, params['output_width'], params['output_height'])
        writer.write(out)
        idx += 1
    cap.release(); writer.release()
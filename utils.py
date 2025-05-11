import cv2

def load_face_cascade(path):
    return cv2.CascadeClassifier(path)


def letterbox(frame, out_w, out_h):
    """letterbox ("contain") mode"""

    h, w = frame.shape[:2]
    scale = min(out_w / w, out_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    top = (out_h - new_h) // 2
    bottom = out_h - new_h - top
    left = (out_w - new_w) // 2
    right = out_w - new_w - left
    return cv2.copyMakeBorder(resized, top, bottom, left, right,
                              cv2.BORDER_CONSTANT, value=[0,0,0])


def detect_largest_face(frame, cascade, scale):
    """face detection and crop center calculation"""
    small = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    return [(int(x/scale), int(y/scale), int(w/scale), int(h/scale)) for (x,y,w,h) in faces]

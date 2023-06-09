import cv2
import matplotlib
matplotlib.use('Qt5Agg')
import parameters as params
from utils.array_util import *


def get_video_clips(video_path):
    frames = get_video_frames(video_path)
    clips = sliding_window(frames, params.frame_count, params.frame_count)
    return clips, len(frames)


def get_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            break
    return frames


def get_stream_video(video_path):
    # camera 정의
    cam = cv2.VideoCapture(video_path)

    while True:
        # 카메라 값 불러오기
        success, frame = cam.read()

        if not success:
            break
        else:
            frame=cv2.resize(frame,(640,360))
            ret, buffer = cv2.imencode('.png', frame)
            # frame을 byte로 변경 후 특정 식으로 변환 후에
            # yield로 하나씩 넘겨준다.
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')

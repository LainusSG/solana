import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
from yolo_prediccion import YOLO_Pred

yolo = YOLO_Pred('./models/best.onnx',
                  './models/data.yml')

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    #flipped = img[::-1,:,:]
    pred_img = yolo.predicciones(img)

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback, media_stream_constraints={"video":True, "audio": False})
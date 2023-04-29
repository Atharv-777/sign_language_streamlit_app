# import cv2
# import time
# import numpy as np
# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
# from keras.models import load_model
# import tensorflow as tf
# import threading as th
# import av

# cnn_model = load_model('cnn_model.h5')
# folders = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

# text_area = st.empty()

# def predict_letter(img):
#     img_for_pred = cv2.resize(img, dsize=(64, 64)).astype('float32')
#     result_arr = cnn_model.predict(np.expand_dims(img_for_pred, axis=0))[0]
#     letter = folders[np.argmax(result_arr)]
#     return letter

# def put_text(text):
#     text_area.write(text)

# class VideoTransformer(VideoTransformerBase):
#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         letter = predict_letter(img)
#         th.Thread(target=put_text, args=(letter,)).start()
#         # put_text(letter)
#         print("reached here....")      
#         return img

# # def display(text):
# #     print(text)

# webrtc_streamer(
#     key="Testing...", 
#     video_processor_factory=VideoTransformer,
#     media_stream_constraints={"video":True, "audio":False}
# )



import concurrent.futures as cf

def plus(a, b):
    return a+b, a*b

def minus():
    return "Hello"

with cf.ThreadPoolExecutor() as executor:
    addition = executor.submit(plus, 6, 5)
    subtraction = executor.submit(minus)
    add_result, multiply = addition.result()
    minus_result = subtraction.result()
    print(add_result)
    print(multiply)
    print(minus_result)
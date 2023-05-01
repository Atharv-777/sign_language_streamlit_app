import streamlit as st
import cv2
import time
import numpy as np
import concurrent.futures as cf
from keras.models import load_model
from streamlit_option_menu import option_menu

st.set_page_config(
    page_icon="icons/translator.png",
    page_title="Sign Language Interpreter"
)

cnn_model = load_model('model/cnn_model.h5')

st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

selected = option_menu(
    menu_title="Main Menu",
    options=['Home','Sign-To-Text','Text-To-Sign'],
    icons=['house','icons/sign-language','icons/animation'],
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    st.title(":blue[Virtual] Sign Language Interpreter..")
    st.write('''
    &emsp; The Virtual Sign Language Interpreter is a :blue[_computer vision_] project that aims to bridge the communication gap between hearing-impaired and 
    non-hearing-impaired people. The project uses computer vision and deep learning to interpret sign language gestures and convert them 
    into spoken language or text. It also supports animation based text to sign language conversion.<br>
    &emsp; For converting Sign to Text, the system uses a camera to capture the sign language gestures made by a user and processes the images using 
    computer vision techniques such as object detection and tracking, feature extraction, and <a href="https://towardsdatascience.com/convolutional-neural-networks-explained-9cc5188c4939" style="text-decoration: none;">_Convolution_</a> 
    to recognize the gestures. The recognized gestures are then translated into spoken language or text, which can be understood by non-hearing-impaired people.<br>
    &emsp; For converting text/speech to sign language, this system uses <a href = "https://cloud.ibm.com/catalog?category=ai" style="text-decoration: none;">_IBM's Watson AI_</a> 
    for taking Speech input from the user and converting it into Text. IBM Watson's Speech-to-Text service supports a variety of languages and accents and can handle a wide range of audio inputs, from telephone-quality 
    recordings to high-quality studio recordings. Once text is generated using Watson AI speech-to-text API, text is used to generate a animated video
    which can be used by non-hearing-impaired people to convery their message to hearing-impaired/deaf people.''', unsafe_allow_html=True)


if selected == "Sign-To-Text":
    folders = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

    # Create a video capture object
    cap = cv2.VideoCapture(0)

    # Set the video resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    st.header("Sign Language to Text..")

    # Create a canvas to display the video frames
    canvas = st.empty()
    text_area = st.empty()
    stop = st.button(label="Stop", key="end_live_stream")

    # Function to detect action in a video frame
    def detect_action(letter):
        ret, frame = cap.read()

        img_for_pred = cv2.resize(frame, dsize=(64, 64)).astype('float32')
        result_arr = cnn_model.predict(np.expand_dims(img_for_pred, axis=0))[0]
        letter = folders[np.argmax(result_arr)]

        return letter

    # To stream the live camera
    def live_stream():
        ret, frame = cap.read()

        if not ret:
            st.error("Error reading the video stream.")
            return

        # Check if the user has clicked the 'Stop' button
        if stop:
            print("clicked stop")
            return frame, False
        
        return frame, True 

    letter = ""
    last_letter = ""
    while True:
        with cf.ThreadPoolExecutor() as executor:
            detect_action_result = executor.submit(detect_action, letter)
            letter = detect_action_result.result()
            if letter in ['del','space','nothing']:
                last_letter += " "
            else:
                last_letter += letter
            text_area.write(last_letter)

            live_stream_result = executor.submit(live_stream)
            frame, result = live_stream_result.result()
            canvas.image(frame, channels="BGR")

            time.sleep(2)
            if not result:
                detect_action_result.cancel()
                live_stream_result.cancel()
                text_area.empty()
                break

    # Release the video capture object and close the Streamlit app
    cap.release()
    cv2.destroyAllWindows()



if selected == "Text-To-Sign":
    st.title(f"Selected {selected}")
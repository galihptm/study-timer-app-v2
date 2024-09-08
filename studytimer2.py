import streamlit as st
import time
import threading
import pygame
from streamlit_javascript import st_javascript

# mixer pygame
pygame.mixer.init()

# alarm
def play_alarm():
    pygame.mixer.music.load('digitalalarmclocksound.mp3')
    pygame.mixer.music.play(-1)  # -1 untuk loop

# alarm stop
def stop_alarm():
    pygame.mixer.music.stop()
    if 'alarm_thread' in st.session_state and st.session_state.alarm_thread:
        st.session_state.alarm_thread.join()  # Tunggu hingga thread selesai

# sesion
if 'alarm_active' not in st.session_state:
    st.session_state.alarm_active = False

if 'alarm_thread' not in st.session_state:
    st.session_state.alarm_thread = None

if 'timer_started' not in st.session_state:
    st.session_state.timer_started = False

st.title("Simple Study Timer App")

hours = st.number_input("Input hour", min_value=0, step=1, value=0)
minutes = st.number_input("Input minute", min_value=0, step=1, value=0)
seconds = st.number_input("Input second", min_value=0, step=1, value=0)

# timer
if st.button("Start Study!"):
    st.session_state.timer_started = True
    total_seconds = hours * 3600 + minutes * 60 + seconds

    if total_seconds == 0:
        st.warning("Input valid time!")
    else:
        st.write(f"Timer is set for {hours} hour(s), {minutes} minute(s), and {seconds} second(s)")
        
        timer_placeholder = st.empty()

        while total_seconds > 0:
            hours_left = total_seconds // 3600
            minutes_left = (total_seconds % 3600) // 60
            seconds_left = total_seconds % 60

            timer_placeholder.text(f"Time remaining: {hours_left} hour(s), {minutes_left} minute(s), {seconds_left} second(s)")
            time.sleep(1)
            total_seconds -= 1

        if not st.session_state.alarm_active:
            st.session_state.alarm_active = True
            st.session_state.alarm_thread = threading.Thread(target=play_alarm)
            st.session_state.alarm_thread.start()

        # popup timeout
        st_javascript('alert("⏰ Time Over!!");')

# stop button
if st.session_state.timer_started:
    if st.button("Stop Alarm"):
        stop_alarm()
        st.session_state.alarm_active = False
        st.session_state.timer_started = False  # Reset timer state
        st.write("Alarm stopped!")

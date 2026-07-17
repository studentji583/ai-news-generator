import streamlit as st
import cv2
import numpy as np
from gtts import gTTS
import os

# Website page config
st.set_page_config(page_title="AI News Video Generator", page_icon="📺", layout="centered")

st.title("📺 Free AI News Video Generator")
st.write("Apni news ka content niche likhein aur professional news video banayein!")

# User Inputs for News
news_headline = st.text_input("🚨 News Headline (Screen par bade aksharon me dikhega)", "BREAKING NEWS")
news_content = st.text_area("✍️ News Details (Jo screen par niche scroll hoga)", "Desh me monsoon ki bhaari baarish ka alert jaari. Aaj kai ilakon me chutti.")
news_voiceover = st.text_area("🗣️ AI News Reporter Voiceover (Hindi me likhein jo AI bolega)", "Namaskar, aap dekh rahe hain AI News. Is waqt ki sabse badi khabar saamne aa rahi hai jahan pure desh me monsoon ka red alert jaari kiya gaya hai.")

if st.button("🎬 Generate News Video"):
    with st.spinner("AI News Studio video taiyar kar raha hai..."):
        
        # 1. Voiceover Generation (Free Text-to-Speech)
        tts = gTTS(text=news_voiceover, lang='hi')
        temp_audio = "news_voice.mp3"
        tts.save(temp_audio)
        
        # Video settings
        output_video = 'ai_news_output.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # HD Resolution (1280x720) at 24 frames per second
        video_writer = cv2.VideoWriter(output_video, fourcc, 24, (1280, 720))
        
        # Video ko 6 second lamba banane ke liye (24 fps * 6 secs = 144 frames)
        total_frames = 144
        
        for frame_num in range(total_frames):
            # Background frame banayein (Dark Studio Grey)
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            frame[:] = (40, 40, 40) 
            
            # 🚨 News Studio Layout Design (Red & Yellow Theme)
            # Top Banner (Headline Box)
            cv2.rectangle(frame, (50, 50), (1230, 150), (0, 0, 255), -1) # Red Box
            cv2.putText(frame, news_headline, (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 5)
            
            # Center Content (News Details)
            cv2.putText(frame, "AI NEWS STUDIO", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)
            
            # Bottom Ticker Tape (Breaking News Banner)
            cv2.rectangle(frame, (0, 620), (1280, 720), (0, 140, 255), -1) # Orange/Yellow Box
            
            # Text ko move (scroll) karwane ka logic
            scroll_speed = 5
            text_x_position = 1280 - (frame_num * scroll_speed)
            if text_x_position < -1500: # Reset text position agar screen se baahar chala jaye
                text_x_position = 1280
                
            cv2.putText(frame, f"LIVE UPDATE: {news_content}", (text_x_position, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 3)
            
            video_writer.write(frame)
            
        video_writer.release()
        
        # Clean up audio file from server
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
            
        st.success("🎉 Aapki AI News Video successfully ban gayi hai!")
        
        # Download Button
        with open(output_video, "rb") as file:
            st.download_button(
                label="📥 Download News MP4 Video",
                data=file,
                file_name="ai_news_video.mp4",
                mime="video/mp4"
            )

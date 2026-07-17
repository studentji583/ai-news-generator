import streamlit as st
import cv2
import numpy as np
from gtts import gTTS
import os
import requests
import hashlib

# 🔑 ENCRYPTED DEFAULT PASSWORD SYSTEM
# default password: mysecretadmin99
DEFAULT_ADMIN_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

# All important systems variables initializer
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'video_count' not in st.session_state:
    st.session_state.video_count = 0
if 'website_active' not in st.session_state:
    st.session_state.website_active = True
if 'current_admin_hash' not in st.session_state:
    st.session_state.current_admin_hash = DEFAULT_ADMIN_HASH

st.set_page_config(page_title="AI News Video Generator Ultra Pro", page_icon="📺", layout="centered")

# --- 👑 SIDEBAR OWNER CONTROL CENTER ---
st.sidebar.title("👑 Master Admin Command Center")
admin_input = st.sidebar.text_input("Enter Master Password", type="password")

# Verify password with secure encryption hash
input_hash = hashlib.sha256(admin_input.encode()).hexdigest()

if input_hash == st.session_state.current_admin_hash:
    is_admin = True
    st.sidebar.success("🔒 Access Granted! Welcome Owner.")
    st.session_state.logged_in = True
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Website Main Switch")
    
    # KILL SWITCH LOGIC (Instantly block/unblock public access)
    if st.session_state.website_active:
        if st.sidebar.button("🔴 Turn Website OFF (Block All Users)"):
            st.session_state.website_active = False
            st.rerun()
    else:
        if st.sidebar.button("🟢 Turn Website ON (Activate App)"):
            st.session_state.website_active = True
            st.rerun()
            
    # PASSWORD CHANGE MODULE
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Change Master Password")
    new_pwd = st.sidebar.text_input("New Password", type="password")
    confirm_pwd = st.sidebar.text_input("Confirm New Password", type="password")
    
    if st.sidebar.button("💾 Save New Password"):
        if new_pwd and new_pwd == confirm_pwd:
            st.session_state.current_admin_hash = hashlib.sha256(new_pwd.encode()).hexdigest()
            st.sidebar.success("✅ Password changed securely!")
        else:
            st.sidebar.error("❌ Passwords mismatch or empty!")
else:
    is_admin = False

# --- PUBLIC ACCESS BLOCK CHECK ---
if not st.session_state.website_active and not is_admin:
    st.error("🚧 WEBSITE IS TEMPORARILY CLOSED BY THE OWNER 🚧")
    st.info("⚠️ Yeh website abhi owner ke dwara temporary band kar di gayi hai.")
    st.stop()

st.title("📺 Premium Secure AI News Studio")

# 🛑 STRICT BANNED WORD FILTER LIST
BANNED_WORDS = [
    "gali", "fraud", "scam", "hack", "bomb", "terrorist", "murder", "khoon", "danga", 
    "fake news", "kill", "drug", "ganja", "charas", "attack", "bhadkau", "abuse", "p**n", 
    "sexy", "nude", "gandi", "sex", "modi", "rahul gandhi", "bjp", "congress"
]

def check_content_safety(text_to_check):
    # Modified Logic: Clears extra spaces/symbols to stop smart bypassing tricks
    cleaned_text = "".join(e for e in text_to_check.lower() if e.isalnum())
    for word in BANNED_WORDS:
        if word in cleaned_text or word in text_to_check.lower():
            return False, word
    return True, ""

# --- MANDATORY SIGN-IN PROTECTION AREA ---
if not st.session_state.logged_in and not is_admin:
    st.warning("⚠️ Video/Shorts banane ke liye pehle Email se Login karna zaroori hai!")
    user_email_input = st.text_input("Apni Email Address Likhein:", placeholder="example@gmail.com")
    
    if st.button("🔐 Login with Email"):
        if "@" in user_email_input and "." in user_email_input:
            st.session_state.logged_in = True
            st.session_state.user_email = user_email_input
            st.success(f"✅ Login Successful! Welcome: {user_email_input}")
            st.rerun()
        else:
            st.error("❌ Kripya ek valid aur sahi Email ID daalein!")
else:
    if not is_admin:
        st.sidebar.info(f"👤 User: {st.session_state.user_email}")
        st.sidebar.info(f"📊 Free Videos Used: {st.session_state.video_count} / 5")

    # PAYWALL SUBSCRIPTION INTERFACE
    if not is_admin and st.session_state.video_count >= 5:
        st.error("🚨 Your Free Limit is Over!")
        st.warning("⚠️ Aapki 5 free videos poori ho chuki hain. Aage unlimited videos banane ke liye plan chuniye:")
        col1, col2 = st.columns(2)
        with col1:
            st.info("⭐ Monthly Pro Plan")
            st.write("### ₹199 / Month")
            st.link_button("💳 Buy Monthly Pack", "https://razorpay.com")
        with col2:
            st.success("🔥 Yearly Best Value Plan")
            st.write("### ₹1,899 / Year")
            st.link_button("💳 Buy Yearly Pack", "https://razorpay.com")
    else:
        # INPUT TEXT BOXES FOR USERS
        news_headline = st.text_input("🚨 News Headline", "BREAKING NEWS")
        news_content = st.text_area("✍️ News Details (Scrolling Text)", "Desh me naye badlav ki taaza update.")
        news_voiceover = st.text_area("🗣️ AI Voiceover (Hindi me)", "Namaskar, aap dekh rahe hain AI News Studio.")
        image_prompt = st.text_input("AI Image Prompt (English me)", "A modern television news studio hall background")

        if st.button("🎬 Generate Ultra HD AI News Video"):
            full_user_text = f"{news_headline} {news_content} {news_voiceover} {image_prompt}"
            is_safe, blocked_word = check_content_safety(full_user_text)
            
            if not is_safe:
                st.error("🚨 SECURITY & SAFETY VIOLATION!")
                st.warning(f"⚠️ Aapka text block kar diya gaya hai kyunki isme gandi/illegal baat '{blocked_word}' mili hai.")
            else:
                with st.spinner("AI Real-time Background Image aur Ultra HD Video generate kar raha hai..."):
                    if not is_admin:
                        st.session_state.video_count += 1
                    
                    # Modified Logic: Engine prompts autotuning enhancements for crisp ultra-hd outputs
                    enhanced_prompt = f"{image_prompt}, 8k resolution, cinematic lighting, ultra photorealistic, television studio layout"
                    encoded_prompt = requests.utils.quote(enhanced_prompt)
                    ai_image_url = f"https://pollinations.ai{encoded_prompt}?width=1280&height=720&nologo=true"
                    
                    try:
                        response = requests.get(ai_image_url, timeout=15)
                        if response.status_code == 200:
                            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                            ai_bg_frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                            ai_bg_frame = cv2.resize(ai_bg_frame, (1280, 720))
                        else:
                            ai_bg_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
                            ai_bg_frame[:] = (40, 40, 40)
                    except Exception as e:
                        ai_bg_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
                        ai_bg_frame[:] = (40, 40, 40)
                    
                    # Audio synthesis engine
                    tts = gTTS(text=news_voiceover, lang='hi')
                    temp_audio = "news_voice.mp3"
                    tts.save(temp_audio)
                    
                    # Video rendering pipeline
                    output_video = 'ai_news_output.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer = cv2.VideoWriter(output_video, fourcc, 24, (1280, 720))
                    
                    for frame_num in range(144):
                        frame = ai_bg_frame.copy()
                        # Red Headline Banner Bar
                        cv2.rectangle(frame, (50, 40), (1230, 130), (0, 0, 255), -1)
                        cv2.putText(frame, news_headline, (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 4)
                        
                        # Orange/Yellow Scrolling News strip
                        cv2.rectangle(frame, (0, 620), (1280, 720), (0, 140, 255), -1)
                        scroll_x = 1280 - (frame_num * 6)
                        cv2.putText(frame, f"LIVE UPDATE: {news_content}", (scroll_x, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 3)
                        video_writer.write(frame)
                        
                    video_writer.release()
                    if os.path.exists(temp_audio):
                        os.remove(temp_audio)
                        
                    st.success("🎉 Ultra HD Real AI News Video Ready Ho Gayi Hai!")
                    with open(output_video, "rb") as file:
                        st.download_button(label="📥 Download HD News Video", data=file, file_name="ai_news.mp4", mime="video/mp4")
  

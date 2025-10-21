import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import math
import os
import requests
import json
from datetime import datetime, timedelta
import pytz
import hashlib

# ============================================================================
# PASSWORD PROTECTION
# ============================================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256("RenaPostTool81".encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show password input with new design
        st.markdown("""
            <style>
                /* CRITICAL: Force hide ALL Streamlit default elements */
                #MainMenu {visibility: hidden !important;}
                footer {visibility: hidden !important;}
                header {visibility: hidden !important;}
                .stDeployButton {visibility: hidden !important;}
                
                /* CRITICAL: Override Streamlit's default background */
                .stApp {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                }
                
                .main {
                    background: transparent !important;
                    padding: 0 !important;
                }
                
                /* FORCE full screen layout - POSITIONED AT TOP */
                .main .block-container {
                    padding: 2rem 1rem !important; 
                    padding-top: 8rem !important;
                    max-width: 100% !important;
                    margin: 0 !important;
                }
                
                /* Remove ALL default Streamlit spacing */
                [data-testid="stVerticalBlock"] {
                    gap: 0 !important;
                }
                
                .element-container {
                    margin: 0 !important;
                }
                
                /* Full viewport height container */
                .login-container {
                    min-height: 100vh;
                    position: relative;
                    overflow: hidden;
                }
                
                /* Animated stars */
                .stars {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1;
                }
                
                .star {
                    position: absolute;
                    width: 3px;
                    height: 3px;
                    background: white;
                    border-radius: 50%;
                    box-shadow: 0 0 4px rgba(255,255,255,0.8);
                }
                
                @keyframes twinkle {
                    0%, 100% { opacity: 0.2; transform: scale(0.8); }
                    50% { opacity: 1; transform: scale(1.2); }
                }
                
                .star:nth-child(1) { animation: twinkle 2s infinite; }
                .star:nth-child(2) { animation: twinkle 3s infinite 0.5s; }
                .star:nth-child(3) { animation: twinkle 2.5s infinite 1s; }
                .star:nth-child(4) { animation: twinkle 3.5s infinite 1.5s; }
                
                /* Login card */
                .login-card {
                    position: relative;
                    z-index: 10;
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    padding: 3rem 2.5rem;
                    border-radius: 24px;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
                    width: 100%;
                    max-width: 450px;
                    margin: 0 auto;
                }
                
                .login-title {
                    color: #2d3748;
                    font-size: 2.5rem;
                    font-weight: 800;
                    text-align: center;
                    margin: 0 0 0.8rem 0;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    letter-spacing: -0.03em;
                    line-height: 1.2;
                }
                
                .login-subtitle {
                    color: rgba(255, 255, 255, 0.95);
                    text-align: center;
                    margin: 0 0 2rem 0;
                    font-size: 1.05rem;
                    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
                    font-weight: 400;
                    letter-spacing: 0.3px;
                }
                
                .login-footer {
                    text-align: center;
                    margin-top: 2rem;
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 0.9rem;
                    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
                }
                
                /* Style the password input - SET CONTAINER WIDTH */
                .stTextInput > div > div > input {
                    background: rgba(255, 255, 255, 0.9) !important;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 255, 255, 0.4) !important;
                    border-radius: 14px !important;
                    color: #2d3748 !important;
                    padding: 16px 20px !important;
                    font-size: 1rem !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                }
                
                .stTextInput {
                    margin: 0 auto !important;
                    width: 340px !important;
                }
                
                .stTextInput > div {
                    display: flex !important;
                    justify-content: center !important;
                    margin: 0 auto !important;
                    width: 340px !important;
                }
                
                .stTextInput > div > div {
                    width: 340px !important;
                }
                
                /* Style the button - EXACT SAME WIDTH AS PASSWORD */
                .stButton {
                    display: block !important;
                    margin-top: 1rem !important;
                    width: 340px !important;
                    margin-left: auto !important;
                    margin-right: auto !important;
                }
                
                .stButton > button {
                    background: white !important;
                    color: #667eea !important;
                    border: 2px solid rgba(200, 200, 220, 0.3) !important;
                    border-radius: 14px !important;
                    padding: 16px 20px !important;
                    font-size: 1rem !important;
                    font-weight: 600 !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    width: 340px !important;
                    letter-spacing: 0.5px !important;
                }
                
                .stButton > button:hover {
                    background: white !important;
                    border-color: #667eea !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
                }
                
                .stButton > button:active {
                    transform: translateY(0) !important;
                }
                
                .stTextInput > div > div > input::placeholder {
                    color: rgba(45, 55, 72, 0.5) !important;
                }
                
                .stTextInput > div > div > input:focus {
                    border-color: #667eea !important;
                    background: white !important;
                    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
                    outline: none !important;
                }
                
                /* Hide label */
                .stTextInput > label {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Stars background
        st.markdown("""
            <div class="stars">
                <div class="star" style="left: 10%; top: 20%;"></div>
                <div class="star" style="left: 20%; top: 40%;"></div>
                <div class="star" style="left: 30%; top: 10%;"></div>
                <div class="star" style="left: 40%; top: 60%;"></div>
                <div class="star" style="left: 50%; top: 30%;"></div>
                <div class="star" style="left: 60%; top: 70%;"></div>
                <div class="star" style="left: 70%; top: 15%;"></div>
                <div class="star" style="left: 80%; top: 50%;"></div>
                <div class="star" style="left: 15%; top: 80%;"></div>
                <div class="star" style="left: 85%; top: 25%;"></div>
                <div class="star" style="left: 25%; top: 75%;"></div>
                <div class="star" style="left: 75%; top: 85%;"></div>
                <div class="star" style="left: 45%; top: 5%;"></div>
                <div class="star" style="left: 55%; top: 90%;"></div>
                <div class="star" style="left: 5%; top: 45%;"></div>
                <div class="star" style="left: 90%; top: 55%;"></div>
                <div class="star" style="left: 35%; top: 65%;"></div>
                <div class="star" style="left: 65%; top: 35%;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Centered login card wrapper
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            st.markdown("""
                <div class="login-card">
                    <h1 class="login-title">All-in-One Content Tool</h1>
                    <p class="login-subtitle">Enter your password to access the tool</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
            
            # Password input
            password_input = st.text_input(
                "Password", 
                type="password",
                key="password",
                placeholder="Enter your password...",
                label_visibility="collapsed"
            )
            
            # Login button
            if st.button("🔓 Login", use_container_width=False, type="primary"):
                if password_input:
                    if hashlib.sha256(password_input.encode()).hexdigest() == hashlib.sha256("RenaPostTool81".encode()).hexdigest():
                        st.session_state["password_correct"] = True
                        st.rerun()
                    else:
                        st.session_state["password_correct"] = False
                        st.rerun()
                else:
                    st.warning("⚠️ Please enter a password")
            
            st.markdown("""
                <div class="login-footer">
                    🔐 Secure access • Content Posting Automations
                </div>
            """, unsafe_allow_html=True)
        
        return False
        
    elif not st.session_state["password_correct"]:
        # Password incorrect
        st.markdown("""
            <style>
                /* CRITICAL: Force hide ALL Streamlit default elements */
                #MainMenu {visibility: hidden !important;}
                footer {visibility: hidden !important;}
                header {visibility: hidden !important;}
                .stDeployButton {visibility: hidden !important;}
                
                /* CRITICAL: Override Streamlit's default background */
                .stApp {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                }
                
                .main {
                    background: transparent !important;
                    padding: 0 !important;
                }
                
                /* FORCE full screen layout - POSITIONED AT TOP */
                .main .block-container {
                    padding: 2rem 1rem !important; 
                    padding-top: 8rem !important;
                    max-width: 100% !important;
                    margin: 0 !important;
                }
                
                /* Remove ALL default Streamlit spacing */
                [data-testid="stVerticalBlock"] {
                    gap: 0 !important;
                }
                
                .element-container {
                    margin: 0 !important;
                }
                
                /* Full viewport height container */
                .login-container {
                    min-height: 100vh;
                    position: relative;
                    overflow: hidden;
                }
                
                /* Animated stars */
                .stars {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1;
                }
                
                .star {
                    position: absolute;
                    width: 3px;
                    height: 3px;
                    background: white;
                    border-radius: 50%;
                    box-shadow: 0 0 4px rgba(255,255,255,0.8);
                }
                
                @keyframes twinkle {
                    0%, 100% { opacity: 0.2; transform: scale(0.8); }
                    50% { opacity: 1; transform: scale(1.2); }
                }
                
                .star:nth-child(1) { animation: twinkle 2s infinite; }
                .star:nth-child(2) { animation: twinkle 3s infinite 0.5s; }
                .star:nth-child(3) { animation: twinkle 2.5s infinite 1s; }
                .star:nth-child(4) { animation: twinkle 3.5s infinite 1.5s; }
                
                /* Shake animation */
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
                    20%, 40%, 60%, 80% { transform: translateX(8px); }
                }
                
                .login-card {
                    position: relative;
                    z-index: 10;
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    padding: 3rem 2.5rem;
                    border-radius: 24px;
                    border: 2px solid rgba(255, 100, 100, 0.5);
                    box-shadow: 0 8px 32px rgba(255, 0, 0, 0.2);
                    width: 100%;
                    max-width: 450px;
                    margin: 0 auto;
                    animation: shake 0.6s;
                }
                
                .login-title {
                    color: #2d3748;
                    font-size: 2.5rem;
                    font-weight: 800;
                    text-align: center;
                    margin: 0 0 0.8rem 0;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    letter-spacing: -0.03em;
                    line-height: 1.2;
                }
                
                .login-subtitle {
                    color: rgba(255, 255, 255, 0.95);
                    text-align: center;
                    margin: 0 0 2rem 0;
                    font-size: 1.05rem;
                    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
                    font-weight: 400;
                    letter-spacing: 0.3px;
                }
                
                .login-footer {
                    text-align: center;
                    margin-top: 2rem;
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 0.9rem;
                    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
                }
                
                /* Style the password input with error state - SET CONTAINER WIDTH */
                .stTextInput > div > div > input {
                    background: rgba(255, 255, 255, 0.9) !important;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 100, 100, 0.7) !important;
                    border-radius: 14px !important;
                    color: #2d3748 !important;
                    padding: 16px 20px !important;
                    font-size: 1rem !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 6px rgba(255,0,0,0.2) !important;
                }
                
                .stTextInput {
                    margin: 0 auto !important;
                    width: 340px !important;
                }
                
                .stTextInput > div {
                    display: flex !important;
                    justify-content: center !important;
                    margin: 0 auto !important;
                    width: 340px !important;
                }
                
                .stTextInput > div > div {
                    width: 340px !important;
                }
                
                /* Style the button - EXACT SAME WIDTH AS PASSWORD */
                .stButton {
                    display: block !important;
                    margin-top: 1rem !important;
                    width: 340px !important;
                    margin-left: auto !important;
                    margin-right: auto !important;
                }
                
                .stButton > button {
                    background: white !important;
                    color: #667eea !important;
                    border: 2px solid rgba(200, 200, 220, 0.3) !important;
                    border-radius: 14px !important;
                    padding: 16px 20px !important;
                    font-size: 1rem !important;
                    font-weight: 600 !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    width: 340px !important;
                    letter-spacing: 0.5px !important;
                }
                
                .stButton > button:hover {
                    background: white !important;
                    border-color: #667eea !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
                }
                
                .stButton > button:active {
                    transform: translateY(0) !important;
                }
                
                .stTextInput > div > div > input::placeholder {
                    color: rgba(45, 55, 72, 0.5) !important;
                }
                
                .stTextInput > div > div > input:focus {
                    border-color: rgba(255, 100, 100, 0.9) !important;
                    background: white !important;
                    box-shadow: 0 0 0 4px rgba(255, 100, 100, 0.15) !important;
                    outline: none !important;
                }
                
                /* Hide label */
                .stTextInput > label {
                    display: none !important;
                }
                
                /* Style error message */
                .stAlert {
                    background: rgba(255, 100, 100, 0.25) !important;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 100, 100, 0.5) !important;
                    border-radius: 12px !important;
                    color: white !important;
                    font-weight: 600 !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Stars background
        st.markdown("""
            <div class="stars">
                <div class="star" style="left: 10%; top: 20%;"></div>
                <div class="star" style="left: 20%; top: 40%;"></div>
                <div class="star" style="left: 30%; top: 10%;"></div>
                <div class="star" style="left: 40%; top: 60%;"></div>
                <div class="star" style="left: 50%; top: 30%;"></div>
                <div class="star" style="left: 60%; top: 70%;"></div>
                <div class="star" style="left: 70%; top: 15%;"></div>
                <div class="star" style="left: 80%; top: 50%;"></div>
                <div class="star" style="left: 15%; top: 80%;"></div>
                <div class="star" style="left: 85%; top: 25%;"></div>
                <div class="star" style="left: 25%; top: 75%;"></div>
                <div class="star" style="left: 75%; top: 85%;"></div>
                <div class="star" style="left: 45%; top: 5%;"></div>
                <div class="star" style="left: 55%; top: 90%;"></div>
                <div class="star" style="left: 5%; top: 45%;"></div>
                <div class="star" style="left: 90%; top: 55%;"></div>
                <div class="star" style="left: 35%; top: 65%;"></div>
                <div class="star" style="left: 65%; top: 35%;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Centered login card wrapper
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            st.markdown("""
                <div class="login-card">
                    <h1 class="login-title">All-in-One Content Tool</h1>
                    <p class="login-subtitle">Enter your password to access the tool</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
            
            # Password input
            password_input = st.text_input(
                "Password", 
                type="password",
                key="password",
                placeholder="Enter your password...",
                label_visibility="collapsed"
            )
            
            # Login button
            if st.button("🔓 Login", use_container_width=False, type="primary"):
                if password_input:
                    if hashlib.sha256(password_input.encode()).hexdigest() == hashlib.sha256("RenaPostTool81".encode()).hexdigest():
                        st.session_state["password_correct"] = True
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password. Please try again.")
                else:
                    st.warning("⚠️ Please enter a password")
            
            st.markdown("""
                <div class="login-footer">
                    🔐 Secure access • Content Posting Automations
                </div>
            """, unsafe_allow_html=True)
        
        return False
        
    else:
        # Password correct
        return True
# ============================================================================
# YOUTUBE TO INSTAGRAM POST FUNCTIONS
# ============================================================================

def create_posts_from_uploads(uploaded_files, post_texts, guest_name="", logo_file=None):
    """Create Instagram posts from uploaded images plus promotional post"""
    
    instagram_posts = []
    
    images = []
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        images.append(img)
    
    for i in range(0, len(images), 2):
        post_images = images[i:i+2]
        post_text = post_texts[i//2] if i//2 < len(post_texts) else ""
        
        instagram_post = create_single_instagram_post(post_images, post_text)
        instagram_posts.append(instagram_post)
    
    # Add promotional post at the end
    if guest_name.strip():
        promo_post = create_promotional_post(guest_name, logo_file)
        instagram_posts.append(promo_post)
    
    return instagram_posts

def create_single_instagram_post(images, post_text):
    """Create a single Instagram post from 1 or 2 images"""
    
    POST_SIZE = 1080
    
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='white')
    
    if len(images) == 2:
        top_img = images[0]
        bottom_img = images[1]
        
        img_height = POST_SIZE // 2
        
        top_img = resize_image_to_exact(top_img, POST_SIZE, img_height)
        bottom_img = resize_image_to_exact(bottom_img, POST_SIZE, img_height)
        
        text_parts = split_text_for_post(post_text)
        
        if len(text_parts) >= 1 and text_parts[0].strip():
            top_img = add_text_overlay(top_img, text_parts[0])
        if len(text_parts) >= 2 and text_parts[1].strip():
            bottom_img = add_text_overlay(bottom_img, text_parts[1])
        
        post.paste(top_img, (0, 0))
        post.paste(bottom_img, (0, POST_SIZE // 2))
        
    else:
        img = images[0]
        img = resize_image_to_exact(img, POST_SIZE, POST_SIZE)
        
        if post_text.strip():
            img = add_text_overlay(img, post_text)
        
        post.paste(img, (0, 0))
    
    return post

def create_promotional_post(guest_name, logo_file=None):
    """Create promotional post with #1A2238 background and #F4DB7D text"""
    
    POST_SIZE = 1080
    
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='#1A2238')
    draw = ImageDraw.Draw(post)
    
    main_text = f'Listen to the full conversation with special guest {guest_name} on the "Rena Malik, MD Podcast"'
    
    main_font_size = 36
    main_font = get_font(main_font_size, bold=True)
    
    max_text_width = POST_SIZE - 120
    wrapped_text = wrap_text(main_text, main_font, max_text_width)
    
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=main_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    logo_height = 0
    if logo_file:
        try:
            logo = Image.open(logo_file)
            logo_max_size = 200
            logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
            logo_height = logo.height + 40
        except:
            logo = None
            logo_height = 0
    else:
        logo = None
    
    available_height = POST_SIZE - logo_height
    text_y = (available_height - text_height) // 2
    if logo:
        text_y += logo_height
    
    text_x = (POST_SIZE - text_width) // 2
    
    shadow_offset = 3
    draw.multiline_text(
        (text_x + shadow_offset, text_y + shadow_offset), 
        wrapped_text, 
        fill='black', 
        font=main_font, 
        align='center'
    )
    draw.multiline_text(
        (text_x, text_y), 
        wrapped_text, 
        fill='#F4DB7D', 
        font=main_font, 
        align='center'
    )
    
    if logo:
        logo_x = (POST_SIZE - logo.width) // 2
        logo_y = 60
        post.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
    
    return post

def split_text_for_post(text):
    """Split text into two roughly equal parts for top and bottom images"""
    if not text.strip():
        return ["", ""]
    
    words = text.split()
    if len(words) <= 1:
        return [text, ""]
    
    mid_point = len(words) // 2
    
    break_point = mid_point
    for i in range(max(1, mid_point - 3), min(len(words), mid_point + 4)):
        if i < len(words) and words[i-1].endswith(('.', '!', '?', ',')):
            break_point = i
            break
    
    first_part = " ".join(words[:break_point])
    second_part = " ".join(words[break_point:])
    
    return [first_part, second_part]

def add_text_overlay(img, text):
    """Add white text with black shadow overlay at the bottom of the image"""
    if not text.strip():
        return img
    
    img_with_text = img.copy()
    if img_with_text.mode != 'RGB':
        img_with_text = img_with_text.convert('RGB')
    
    draw = ImageDraw.Draw(img_with_text)
    
    img_width, img_height = img.size
    
    font_size = max(24, min(44, img_width // 25))
    
    font = get_font(font_size)
    
    max_text_width = img_width - 60
    wrapped_text = wrap_text(text, font, max_text_width)
    
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    margin_bottom = 25
    margin_side = 30
    
    text_x = (img_width - text_width) // 2
    text_y = img_height - text_height - margin_bottom
    
    max_text_height = img_height * 0.3
    min_y = img_height * 0.7
    
    if text_height > max_text_height:
        text_y = max(min_y, img_height - max_text_height - margin_bottom)
    
    text_x = max(margin_side, min(text_x, img_width - text_width - margin_side))
    text_y = min(text_y, img_height - text_height - margin_bottom)
    
    bg_margin = 15
    bg_coords = [
        max(0, text_x - bg_margin),
        max(0, text_y - bg_margin),
        min(img_width, text_x + text_width + bg_margin),
        min(img_height, text_y + text_height + bg_margin)
    ]
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(bg_coords, fill=(0, 0, 0, 120))
    
    img_with_text = Image.alpha_composite(img_with_text.convert('RGBA'), overlay).convert('RGB')
    
    draw = ImageDraw.Draw(img_with_text)
    shadow_offset = 2
    
    draw.multiline_text(
        (text_x + shadow_offset, text_y + shadow_offset), 
        wrapped_text, 
        fill='black', 
        font=font, 
        align='center'
    )
    draw.multiline_text(
        (text_x, text_y), 
        wrapped_text, 
        fill='white', 
        font=font, 
        align='center'
    )
    
    return img_with_text

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width with better line breaking"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        
        try:
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(test_line) * (font.size * 0.6)
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    if len(lines) > 5:
        lines = lines[:4] + [lines[4] + "..."]
    
    return '\n'.join(lines)

def resize_image_to_exact(img, target_width, target_height):
    """Resize image to exact dimensions, cropping if necessary to maintain aspect ratio"""
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        new_height = target_height
        new_width = int(target_height * img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        left = (new_width - target_width) // 2
        cropped = resized.crop((left, 0, left + target_width, target_height))
        
    else:
        new_width = target_width
        new_height = int(target_width / img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        top = (new_height - target_height) // 2
        cropped = resized.crop((0, top, target_width, top + target_height))
    
    return cropped

def pil_to_bytes(img):
    """Convert PIL Image to bytes for download with error handling"""
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG', quality=95, optimize=True)
        img_bytes.seek(0)
        return img_bytes.getvalue()
    except Exception as e:
        st.error(f"Error converting image: {str(e)}")
        try:
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG', optimize=True)
            img_bytes.seek(0)
            return img_bytes.getvalue()
        except:
            return None

def create_zip_from_posts(instagram_posts, original_images=None):
    """Create zip file with Instagram posts and optionally original images"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, post_img in enumerate(instagram_posts):
            filename = f"instagram_posts/post_{i+1}.jpg"
            img_bytes = pil_to_bytes(post_img)
            if img_bytes:
                zip_file.writestr(filename, img_bytes)
        
        if original_images:
            for i, img_file in enumerate(original_images):
                try:
                    filename = f"original_screenshots/screenshot_{i+1}.jpg"
                    img = Image.open(img_file)
                    img_bytes = pil_to_bytes(img)
                    if img_bytes:
                        zip_file.writestr(filename, img_bytes)
                except Exception as e:
                    st.warning(f"Could not include original image {i+1}: {str(e)}")
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# ============================================================================
# MULTI-PLATFORM POSTING FUNCTIONS
# ============================================================================

def upload_image_to_getlate(image_file, api_key):
    """Upload image to GetLate media endpoint and return URL"""
    try:
        # Reset file pointer to beginning
        image_file.seek(0)
        
        # Prepare the file for upload
        files = {'files': (image_file.name, image_file, 'image/jpeg')}
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # Upload to GetLate
        response = requests.post(
            "https://getlate.dev/api/v1/media",
            headers=headers,
            files=files
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            # Return the URL from the response
            return result['files'][0]['url']
        else:
            st.error(f"Failed to upload image: {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error uploading image: {str(e)}")
        return None

def send_post_to_api(api_key, post_data):
    """Send post to GetLate API"""
    endpoint = "https://getlate.dev/api/v1/posts"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=post_data)
        return response
    except Exception as e:
        return None

def build_post_payload(content, scheduled_time, timezone, platforms_config):
    """Build the JSON payload for the API request"""
    payload = {
        "content": content,
        "scheduledFor": scheduled_time,
        "timezone": timezone,
        "platforms": []
    }
    
    for platform_data in platforms_config:
        platform_entry = {
            "accountId": platform_data["accountId"],
            "mediaItems": platform_data.get("mediaItems", [])
        }
        payload["platforms"].append(platform_entry)
    
    return payload

# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(
    page_title="Content Posting Automations", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"  # Force sidebar to be open by default
)

# Check password first
if not check_password():
    st.stop()  # Stop execution if password is incorrect

# Custom CSS for modern, beautiful styling
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Toggle Button - Make it more visible */
    button[kind="header"] {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
    
    button[kind="header"]:hover {
        background: #667eea !important;
        color: white !important;
        transform: scale(1.05);
    }
    
    /* Sidebar collapse/expand button - ENHANCED VISIBILITY */
    [data-testid="collapsedControl"] {
        background: white !important;
        color: #667eea !important;
        border: 3px solid #667eea !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2) !important;
        width: 40px !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #667eea !important;
        color: white !important;
        border-color: #764ba2 !important;
        box-shadow: 2px 2px 16px rgba(102, 126, 234, 0.4) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Make sidebar toggle arrow more visible when sidebar is open */
    [data-testid="stSidebar"] button[kind="header"] {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
    }
    
    [data-testid="stSidebar"] button[kind="header"]:hover {
        background: rgba(255,255,255,0.3) !important;
        border-color: white !important;
    }
    
    /* Main Container - Fixed layout with sidebar always visible */
    .main {
        background: #f5f7fa;
        padding: 0 !important;
        margin-left: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        background: #f5f7fa;
        margin: 0 auto !important;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        text-align: center;
        color: #4a5568;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 28px;
        background: transparent;
        border-radius: 12px;
        color: #2d3748;
        font-size: 16px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f5f7fa;
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        font-weight: 700 !important;
    }
    
    /* Force tab text colors - CRITICAL FIX */
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div {
        color: #2d3748 !important;
    }
    
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] div {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] > div,
    .stTabs [data-baseweb="tab"] > div > div {
        color: inherit !important;
    }
    
    /* Additional override for any nested elements */
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Sidebar Styling - FIXED, NO TOGGLE */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-right: none;
        min-width: 21rem !important;
        max-width: 21rem !important;
        transform: none !important;
        margin-left: 0 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    /* HIDE all toggle buttons - sidebar cannot be collapsed */
    section[data-testid="stSidebar"] button[kind="header"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Prevent sidebar from collapsing */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 21rem !important;
        max-width: 21rem !important;
        margin-left: 0 !important;
    }
    
    /* Style the sidebar collapse/expand button - Make it VISIBLE and working */
    section[data-testid="stSidebar"] button[kind="header"] {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    section[data-testid="stSidebar"] button[kind="header"]:hover {
        background: rgba(255,255,255,0.3) !important;
        border-color: white !important;
        transform: scale(1.05);
    }
    
    /* Add tooltip text to sidebar button */
    section[data-testid="stSidebar"] button[kind="header"]::after {
        content: "Hide Sidebar";
        position: absolute;
        left: 100%;
        top: 50%;
        transform: translateY(-50%);
        margin-left: 10px;
        background: #2d3748;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 999;
    }
    
    section[data-testid="stSidebar"] button[kind="header"]:hover::after {
        opacity: 1;
    }
    
    /* Sidebar collapse/expand button when sidebar is CLOSED */
    [data-testid="collapsedControl"] {
        background: white !important;
        color: #667eea !important;
        border: 3px solid #667eea !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2) !important;
        width: 40px !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #667eea !important;
        color: white !important;
        border-color: #764ba2 !important;
        box-shadow: 2px 2px 16px rgba(102, 126, 234, 0.4) !important;
        transform: scale(1.05);
    }
    
    [data-testid="collapsedControl"] svg {
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Add tooltip text to collapsed control */
    [data-testid="collapsedControl"]::after {
        content: "Open Sidebar";
        position: absolute;
        left: 100%;
        top: 50%;
        transform: translateY(-50%);
        margin-left: 10px;
        background: #2d3748;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 999;
    }
    
    [data-testid="collapsedControl"]:hover::after {
        opacity: 1;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] a {
        color: rgba(255, 255, 255, 0.9) !important;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] a:hover {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] small {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.2s ease;
        background: white;
        color: #1a202c;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Labels */
    label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 15px;
        border: none;
        transition: all 0.3s ease;
        text-transform: none;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5568d3 0%, #65408b 100%);
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #667eea !important;
        border: 2px solid #667eea;
    }
    
    /* Force button text to be visible */
    .stButton > button span,
    .stButton > button p,
    .stButton > button div {
        color: inherit !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        border-radius: 16px;
        border: 2px dashed #667eea;
        padding: 2rem;
        background: #f7fafc;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #764ba2;
        background: #edf2f7;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 12px;
        background: #f7fafc;
        font-weight: 600;
        border: none;
        padding: 16px 20px;
        color: #2d3748;
    }
    
    .streamlit-expanderHeader:hover {
        background: #edf2f7;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Success/Error/Info Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 16px 20px;
        border: none;
        font-weight: 500;
    }
    
    .stSuccess {
        background: #d4edda;
        color: #155724;
    }
    
    .stError {
        background: #f8d7da;
        color: #721c24;
    }
    
    .stInfo {
        background: #d1ecf1;
        color: #0c5460;
    }
    
    .stWarning {
        background: #fff3cd;
        color: #856404;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: #e2e8f0;
    }
    
    /* Headers in content */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #1a202c;
    }
    
    h1 {
        color: #1a1a2e;
    }
    
    h2 {
        color: #2d3748;
    }
    
    h3 {
        color: #4a5568;
    }
    
    p {
        color: #4a5568;
    }
    
    /* Code blocks */
    code {
        background: #f7fafc;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.9em;
        color: #667eea;
        font-weight: 500;
    }
    
    /* Caption text */
    .stCaption {
        color: #718096 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 Content Posting Automations</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Streamline your content creation and multi-platform posting workflow</p>', unsafe_allow_html=True)

# Hidden component to load data from localStorage
load_storage_js = """
<script>
    const apiKey = localStorage.getItem('api_key') || '';
    const igId = localStorage.getItem('ig_account_id') || '';
    const liId = localStorage.getItem('li_account_id') || '';
    const fbId = localStorage.getItem('fb_account_id') || '';
    const twId = localStorage.getItem('tw_account_id') || '';
    
    // Store in hidden inputs to pass to Streamlit
    if (apiKey) document.cookie = `api_key=${apiKey}; path=/`;
    if (igId) document.cookie = `ig_account_id=${igId}; path=/`;
    if (liId) document.cookie = `li_account_id=${liId}; path=/`;
    if (fbId) document.cookie = `fb_account_id=${fbId}; path=/`;
    if (twId) document.cookie = `tw_account_id=${twId}; path=/`;
</script>
"""
st.components.v1.html(load_storage_js, height=0)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'master_content' not in st.session_state:
    st.session_state.master_content = ""
if 'master_schedule' not in st.session_state:
    st.session_state.master_schedule = None
# Save account IDs (will be loaded from localStorage)
if 'ig_account_id' not in st.session_state:
    st.session_state.ig_account_id = ""
if 'li_account_id' not in st.session_state:
    st.session_state.li_account_id = ""
if 'fb_account_id' not in st.session_state:
    st.session_state.fb_account_id = ""
if 'tw_account_id' not in st.session_state:
    st.session_state.tw_account_id = ""
# Tab 1 Instagram posting
if 'generated_ig_posts' not in st.session_state:
    st.session_state.generated_ig_posts = None
if 'show_ig_posting' not in st.session_state:
    st.session_state.show_ig_posting = False
if 'post_texts_for_ig' not in st.session_state:
    st.session_state.post_texts_for_ig = []

# Load from localStorage on first load
if 'loaded_from_storage' not in st.session_state:
    st.session_state.loaded_from_storage = True

# API Key in sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    api_key = st.text_input(
        "🔑 GetLate API Key", 
        type="password", 
        value=st.session_state.api_key,
        help="Enter your GetLate API key for posting",
        placeholder="Enter your API key...",
        key="api_key_input"
    )
    
    # Save to both session state and localStorage
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        if api_key:
            save_to_localstorage('api_key', api_key)
    
    if api_key:
        st.success("✅ Connected & Saved Permanently")
    else:
        st.warning("⚠️ API key required")
    
    st.markdown("---")
    st.markdown("### 📚 Resources")
    st.markdown("🔗 [GetLate Dashboard](https://getlate.dev/dashboard)")
    st.markdown("📖 [API Documentation](https://getlate.dev/docs)")
    st.markdown("💬 [Support](mailto:miki@getlate.dev)")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    if st.session_state.api_key:
        st.info("🟢 API Connected")
    else:
        st.error("🔴 No API Key")
    
    # Show saved account IDs
    saved_accounts = []
    if st.session_state.ig_account_id:
        saved_accounts.append("📷 Instagram")
    if st.session_state.li_account_id:
        saved_accounts.append("💼 LinkedIn")
    if st.session_state.fb_account_id:
        saved_accounts.append("👥 Facebook")
    if st.session_state.tw_account_id:
        saved_accounts.append("🐦 Twitter")
    
    if saved_accounts:
        st.success(f"💾 {len(saved_accounts)} accounts saved")
        with st.expander("View Saved Accounts"):
            for account in saved_accounts:
                st.write(account)
            
            st.markdown("---")
            st.warning("⚠️ Clearing will remove API key and all account IDs")
            if st.button("🗑️ Clear All Saved Data", use_container_width=True):
                st.session_state.api_key = ""
                st.session_state.ig_account_id = ""
                st.session_state.li_account_id = ""
                st.session_state.fb_account_id = ""
                st.session_state.tw_account_id = ""
                clear_localstorage()
                st.success("✅ All data cleared!")
                st.rerun()
    else:
        st.info("No accounts saved yet")
    
    st.markdown("---")
    st.markdown("<small>Made with ❤️ for content creators</small>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 YouTube to Instagram", 
    "🎙️ CTA Podcast Content",
    "🎨 Create Carousel/Feed Post", 
    "🎬 Create Short Form Video Post"
])

# ============================================================================
# TAB 1: YOUTUBE TO INSTAGRAM
# ============================================================================

with tab1:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📸 YouTube to Instagram</h1>
            <p style='font-size: 1.1rem; color: #666;'>Transform your YouTube screenshots into stunning Instagram carousel posts</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Upload section with modern card
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>📤 Upload Your Screenshots</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Pro Tips for Amazing Screenshots", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📸 Taking Screenshots:**
            - 🖥️ Go fullscreen for quality
            - ⏸️ Pause at key moments
            - 🎯 Use 2 screenshots per post
            - 💾 Save as PNG or JPG
            """)
        with col2:
            st.markdown("""
            **⌨️ Keyboard Shortcuts:**
            - **Windows:** `Win + Shift + S`
            - **Mac:** `Cmd + Shift + 4`
            - **Mobile:** `Power + Vol Down`
            """)
    
    uploaded_files = st.file_uploader(
        "📁 Drop your screenshots here or click to browse", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg'],
        help="Upload in the order you want them to appear"
    )
    
    if uploaded_files:
        # Stats cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📷 Images Uploaded", len(uploaded_files))
        with col2:
            num_posts = math.ceil(len(uploaded_files) / 2)
            st.metric("📱 Posts to Create", num_posts)
        with col3:
            st.metric("⚡ Images per Post", "2")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Image preview in a nice grid
        st.markdown("### 🖼️ Your Screenshots")
        cols = st.columns(4)
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 4]:
                img = Image.open(uploaded_file)
                st.image(img, caption=f"Screenshot {i+1}", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Text input section with modern styling
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
                <h3 style='margin-top: 0;'>✍️ Add Captions to Your Posts</h3>
            </div>
        """, unsafe_allow_html=True)
        num_posts = math.ceil(len(uploaded_files) / 2)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            post_texts_input = st.text_area(
                f"📝 Enter captions for your {num_posts} posts", 
                placeholder="Caption for post 1 (will split across 2 images)\nCaption for post 2\nCaption for post 3...",
                height=150,
                help="One line per post. Text automatically splits between images."
            )
        
        with col2:
            st.markdown("**🎨 Customization Options**")
            include_originals = st.checkbox("📦 Include originals in ZIP", value=True)
            guest_name = st.text_input("👤 Guest name (optional)", placeholder="Dr. Jane Smith")
            logo_file = st.file_uploader("🎭 Podcast logo (optional)", type=['png', 'jpg', 'jpeg'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create button with modern styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎨 ✨ Generate Instagram Posts", type="primary", use_container_width=True):
                post_texts = [line.strip() for line in post_texts_input.split('\n') if line.strip()]
                
                with st.spinner("✨ Creating your beautiful Instagram posts..."):
                    instagram_posts = create_posts_from_uploads(
                        uploaded_files, 
                        post_texts, 
                        guest_name, 
                        logo_file
                    )
                    
                    # Store in session state for posting later
                    st.session_state.generated_ig_posts = instagram_posts
                    st.session_state.post_texts_for_ig = post_texts
                    
                    st.success(f"🎉 Successfully created {len(instagram_posts)} Instagram posts!")
                    
                    # Show preview in a beautiful grid
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 👀 Preview Your Amazing Posts")
                    cols = st.columns(3)
                    for i, post_img in enumerate(instagram_posts):
                        with cols[i % 3]:
                            st.image(post_img, caption=f"Post {i+1}", use_container_width=True)
                    
                    # Download section with modern card
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                                    padding: 2rem; border-radius: 16px; text-align: center;'>
                            <h3 style='margin-top: 0;'>📥 Download or Post to Instagram</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        original_imgs = uploaded_files if include_originals else None
                        zip_data = create_zip_from_posts(instagram_posts, original_imgs)
                        
                        st.download_button(
                            label="⬇️ Download All Posts (ZIP)",
                            data=zip_data,
                            file_name=f"instagram_posts_{len(instagram_posts)}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("📸 Post to Instagram", type="secondary", use_container_width=True):
                            st.session_state.show_ig_posting = True
                            st.rerun()
                    
                    st.info(f"""
                    **📦 Your download includes:**
                    - ✅ {len(instagram_posts)} Instagram-ready posts (1080x1080px)
                    - {"✅ Original screenshots included" if include_originals else ""}
                    - ✅ Ready to upload to Instagram instantly!
                    """)
        
        # Instagram Posting Section
        if st.session_state.get('show_ig_posting') and st.session_state.get('generated_ig_posts'):
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                <div style='background: linear-gradient(135deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); 
                            padding: 0.1rem; border-radius: 16px; margin: 2rem 0;'>
                    <div style='background: white; padding: 2rem; border-radius: 15px;'>
                        <h3 style='margin-top: 0; color: #bc1888; text-align: center;'>📷 Post to Instagram</h3>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if not st.session_state.api_key:
                st.warning("⚠️ Please enter your GetLate API Key in the sidebar to post to Instagram")
            elif not st.session_state.ig_account_id:
                st.warning("⚠️ Please enter your Instagram Account ID in the sidebar settings")
                with st.expander("How to get your Instagram Account ID"):
                    st.markdown("""
                    1. Go to the **Create Carousel/Feed Post** tab
                    2. Enable Instagram and enter your Account ID
                    3. It will be saved for future use
                    
                    Or get it via API:
                    ```
                    curl -H "Authorization: Bearer YOUR_API_KEY" \
                      "https://getlate.dev/api/v1/accounts?profileId=PROFILE_ID"
                    ```
                    """)
            else:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    ig_caption_tab1 = st.text_area(
                        "📝 Instagram Caption",
                        value="",
                        height=120,
                        placeholder="Write your Instagram caption here...\n\nAdd hashtags and emojis! 🎉",
                        key="ig_caption_tab1"
                    )
                
                with col2:
                    st.markdown("**📅 Schedule**")
                    
                    post_now_tab1 = st.checkbox("Post Immediately", value=True, key="post_now_tab1")
                    
                    if not post_now_tab1:
                        default_date = datetime.now() + timedelta(hours=1)
                        pdt = pytz.timezone('America/Los_Angeles')
                        
                        schedule_date_tab1 = st.date_input("Date", value=default_date, key="schedule_date_tab1")
                        schedule_time_tab1 = st.time_input("Time (PDT)", value=default_date.time(), key="schedule_time_tab1")
                        
                        schedule_datetime = datetime.combine(schedule_date_tab1, schedule_time_tab1)
                        schedule_datetime_pdt = pdt.localize(schedule_datetime)
                        schedule_iso_tab1 = schedule_datetime_pdt.isoformat()
                    else:
                        schedule_iso_tab1 = None
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.info(f"📊 {len(st.session_state.generated_ig_posts)} posts will be uploaded")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Post to Instagram button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Post All to Instagram Now", type="primary", use_container_width=True, key="post_to_ig_btn"):
                        with st.spinner("📤 Uploading images and posting to Instagram..."):
                            success_count = 0
                            error_count = 0
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Upload each generated post to GetLate and schedule
                            for idx, post_img in enumerate(st.session_state.generated_ig_posts):
                                status_text.text(f"Uploading post {idx + 1} of {len(st.session_state.generated_ig_posts)}...")
                                
                                # Convert PIL Image to bytes
                                img_bytes_io = BytesIO()
                                post_img.save(img_bytes_io, format='JPEG', quality=95)
                                img_bytes_io.seek(0)
                                
                                # Create a file-like object for upload
                                img_bytes_io.name = f"instagram_post_{idx + 1}.jpg"
                                
                                # Upload to GetLate
                                uploaded_url = upload_image_to_getlate(img_bytes_io, st.session_state.api_key)
                                
                                if uploaded_url:
                                    # Create post payload
                                    post_payload = {
                                        "content": ig_caption_tab1 if ig_caption_tab1 else f"Post {idx + 1}",
                                        "platforms": [
                                            {
                                                "platform": "instagram",
                                                "accountId": st.session_state.ig_account_id,
                                                "mediaItems": [{"url": uploaded_url}]
                                            }
                                        ],
                                        "timezone": "America/Los_Angeles"
                                    }
                                    
                                    if post_now_tab1:
                                        post_payload["publishNow"] = True
                                    else:
                                        post_payload["scheduledFor"] = schedule_iso_tab1
                                    
                                    # Send to GetLate API
                                    response = send_post_to_api(st.session_state.api_key, post_payload)
                                    
                                    if response and response.status_code in [200, 201]:
                                        success_count += 1
                                    else:
                                        error_count += 1
                                        st.error(f"❌ Post {idx + 1} failed to schedule")
                                else:
                                    error_count += 1
                                    st.error(f"❌ Failed to upload post {idx + 1}")
                                
                                progress_bar.progress((idx + 1) / len(st.session_state.generated_ig_posts))
                            
                            status_text.empty()
                            progress_bar.empty()
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            if error_count == 0:
                                st.balloons()
                                st.markdown("""
                                    <div style='background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                                padding: 2rem; border-radius: 16px; text-align: center;'>
                                        <h2 style='margin: 0; color: #155724;'>🎉 Success!</h2>
                                        <p style='color: #155724; margin: 0.5rem 0 0 0;'>All {success_count} posts posted to Instagram successfully!</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                                                padding: 2rem; border-radius: 16px; text-align: center;'>
                                        <h3 style='margin: 0; color: #856404;'>⚠️ Partial Success</h3>
                                        <p style='color: #856404; margin: 0.5rem 0 0 0;'>{success_count} successful, {error_count} failed</p>
                                    </div>
                                """, unsafe_allow_html=True)
                
                # Close button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌ Close Instagram Posting", use_container_width=True):
                    st.session_state.show_ig_posting = False
                    st.rerun()

# ============================================================================
# TAB 2: CTA PODCAST CONTENT CREATION
# ============================================================================

with tab2:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎙️ CTA Podcast Content Creation</h1>
            <p style='font-size: 1.1rem; color: #666;'>Create engaging call-to-action content for your podcast episodes</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
            <h2 style='margin: 0; color: #667eea;'>🚧 Coming Soon</h2>
            <p style='color: #666; margin: 1rem 0 0 0; font-size: 1.1rem;'>This feature is currently under development</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Placeholder content
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 2rem 0;'>
            <h3 style='margin-top: 0;'>📋 Planned Features:</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎨 Content Creation
        - 📝 Custom CTA templates
        - 🖼️ Branded graphics generator
        - ✂️ Podcast clip creator
        - 📊 Episode highlights extractor
        - 🎯 Audience engagement tools
        """)
        
        st.markdown("""
        ### 🎙️ Podcast Specific
        - 🎵 Audio waveform visualizer
        - 📢 Guest spotlight creator
        - 🔊 Episode teaser generator
        - 💬 Quote card maker
        - 🎧 Listen now CTAs
        """)
    
    with col2:
        st.markdown("""
        ### 📱 Social Media Ready
        - 📸 Instagram story templates
        - 🎬 Reel/Short form video CTAs
        - 🖼️ Carousel post builder
        - 📝 Caption suggestions
        - #️⃣ Hashtag recommendations
        """)
        
        st.markdown("""
        ### 🚀 Automation
        - ⏰ Scheduled content drops
        - 🔄 Auto-post episode releases
        - 📧 Email newsletter integration
        - 📊 Analytics tracking
        - 🎯 A/B testing CTAs
        """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Interactive placeholder
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 2rem 0;'>
            <h3 style='margin-top: 0; text-align: center;'>💡 Got Ideas?</h3>
            <p style='text-align: center; color: #666;'>Help shape this feature! What podcast CTA tools would you find most valuable?</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_suggestions = st.text_area(
        "Share your suggestions (optional)",
        placeholder="What features would make your podcast content creation easier?",
        height=100
    )
    
    if st.button("📧 Send Suggestions", type="primary", use_container_width=True):
        if user_suggestions:
            st.success("✅ Thank you! Your suggestions have been noted.")
            st.balloons()
        else:
            st.info("💡 Please enter your suggestions above")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; color: white;'>
            <h2 style='margin: 0 0 1rem 0; color: white;'>🎙️ Stay Tuned!</h2>
            <p style='margin: 0 0 1.5rem 0; font-size: 1.1rem;'>We're working hard to bring you the best podcast CTA tools</p>
            <p style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>Expected release: Coming Soon</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: CREATE CAROUSEL/FEED POST
# ============================================================================
# ============================================================================
# TAB 3: CREATE CAROUSEL/FEED POST - COMPLETE CODE WITH FIXES
# ============================================================================

with tab3:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎨 Multi-Platform Post Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>Upload once, post everywhere. Reach your audience across all platforms</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not st.session_state.api_key:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                        padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
                <h3 style='margin: 0; color: #856404;'>⚠️ API Key Required</h3>
                <p style='color: #856404; margin: 0.5rem 0 0 0;'>Please enter your GetLate API Key in the sidebar to use this feature</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Image upload section with modern card
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>📤 Upload Your Media</h3>
        </div>
    """, unsafe_allow_html=True)    
    carousel_images = st.file_uploader(
        "📁 Drop your images here or click to browse",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        key="carousel_images",
        help="Upload images for your carousel or feed post"
    )
    
    if carousel_images:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ {len(carousel_images)} image(s) uploaded successfully")
        with col2:
            st.metric("📷 Total Images", len(carousel_images))
        
        # FIXED: Compact image preview in collapsible grid
        with st.expander(f"👁️ Preview Uploaded Images ({len(carousel_images)} images)", expanded=False):
            # Show in grid of 4 columns
            num_cols = 4
            cols = st.columns(num_cols)
            for i, img_file in enumerate(carousel_images):
                with cols[i % num_cols]:
                    img = Image.open(img_file)
                    st.image(img, use_container_width=True, caption=f"#{i+1}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Master content editor with modern styling
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0; border: 2px solid #667eea;'>
            <h3 style='margin-top: 0; color: #667eea;'>📝 Master Content Editor</h3>
            <p style='color: #4a5568; margin: 0.5rem 0 0 0; font-size: 0.95rem;'>
                ✍️ Create your content once, then push to all selected platforms below
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        master_content = st.text_area(
            "✍️ Post Content",
            value=st.session_state.master_content,
            height=150,
            placeholder="Write your post content here... This will be your default content for all platforms.",
            key="master_content_input"
        )
        st.session_state.master_content = master_content
    
    with col2:
        st.markdown("**📅 Master Schedule (PDT)**")
        
        # FIXED: Use unique keys and store in session state properly
        default_date = datetime.now() + timedelta(hours=1)
        
        master_date = st.date_input(
            "📆 Date", 
            value=default_date,
            key="master_date_input"
        )
        master_time = st.time_input(
            "🕐 Time", 
            value=default_date.time(),
            key="master_time_input"
        )
        
        # Combine date and time
        master_datetime = datetime.combine(master_date, master_time)
        pdt = pytz.timezone('America/Los_Angeles')
        master_datetime_pdt = pdt.localize(master_datetime)
        master_schedule_iso = master_datetime_pdt.isoformat()
        
        st.session_state.master_schedule = master_schedule_iso
    
    # Post to All Platforms Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2.5rem; border-radius: 16px; text-align: center; margin: 1.5rem 0;
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);'>
            <h3 style='margin: 0 0 0.5rem 0; color: #ffffff; font-size: 1.5rem; font-weight: 700;'>
                🚀 Post Content to All Platforms
            </h3>
            <p style='margin: 0; font-size: 1rem; color: #ffffff; opacity: 1;'>
                Click below to post your master content to all configured platforms at once
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Post to All Selected Platforms", use_container_width=True, type="primary", key="push_to_all_btn"):
            if not st.session_state.api_key:
                st.error("❌ Please enter your API key in the sidebar!")
            else:
                # Build list of platforms to post to
                platforms_to_post = []
                
                if enable_instagram and st.session_state.get('ig_account_id'):
                    # Upload images first
                    media_items = []
                    if carousel_images:
                        with st.spinner("📤 Uploading images for Instagram..."):
                            for img in carousel_images:
                                url = upload_image_to_getlate(img, st.session_state.api_key)
                                if url:
                                    media_items.append({"url": url})
                    
                    platforms_to_post.append({
                        "platform": "Instagram",
                        "accountId": st.session_state.ig_account_id,
                        "content": st.session_state.master_content,
                        "schedule": st.session_state.master_schedule,
                        "mediaItems": media_items
                    })
                
                if enable_linkedin and st.session_state.get('li_account_id'):
                    # Upload images first
                    media_items = []
                    if carousel_images:
                        with st.spinner("📤 Uploading images for LinkedIn..."):
                            for img in carousel_images:
                                url = upload_image_to_getlate(img, st.session_state.api_key)
                                if url:
                                    media_items.append({"url": url})
                    
                    platforms_to_post.append({
                        "platform": "LinkedIn",
                        "accountId": st.session_state.li_account_id,
                        "content": st.session_state.master_content,
                        "schedule": st.session_state.master_schedule,
                        "mediaItems": media_items
                    })
                
                if enable_facebook and st.session_state.get('fb_account_id'):
                    # Upload images first
                    media_items = []
                    if carousel_images:
                        with st.spinner("📤 Uploading images for Facebook..."):
                            for img in carousel_images:
                                url = upload_image_to_getlate(img, st.session_state.api_key)
                                if url:
                                    media_items.append({"url": url})
                    
                    platforms_to_post.append({
                        "platform": "Facebook",
                        "accountId": st.session_state.fb_account_id,
                        "content": st.session_state.master_content,
                        "schedule": st.session_state.master_schedule,
                        "mediaItems": media_items
                    })
                
                if enable_twitter and st.session_state.get('tw_account_id'):
                    # Upload images first
                    media_items = []
                    if carousel_images:
                        with st.spinner("📤 Uploading images for Twitter..."):
                            for img in carousel_images:
                                url = upload_image_to_getlate(img, st.session_state.api_key)
                                if url:
                                    media_items.append({"url": url})
                    
                    platforms_to_post.append({
                        "platform": "Twitter",
                        "accountId": st.session_state.tw_account_id,
                        "content": st.session_state.master_content,
                        "schedule": st.session_state.master_schedule,
                        "mediaItems": media_items
                    })
                
                if not platforms_to_post:
                    st.error("❌ No platforms configured! Please enable platforms and enter Account IDs.")
                else:
                    # Post to all platforms
                    with st.spinner(f"📤 Posting to {len(platforms_to_post)} platform(s)..."):
                        success_count = 0
                        error_count = 0
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, platform_data in enumerate(platforms_to_post):
                            status_text.text(f"Posting to {platform_data['platform']}...")
                            
                            payload = build_post_payload(
                                content=platform_data['content'],
                                scheduled_time=platform_data['schedule'],
                                timezone="America/Los_Angeles",
                                platforms_config=[{
                                    "accountId": platform_data['accountId'],
                                    "mediaItems": platform_data['mediaItems']
                                }]
                            )
                            
                            response = send_post_to_api(st.session_state.api_key, payload)
                            
                            if response and response.status_code in [200, 201]:
                                success_count += 1
                            else:
                                error_count += 1
                                error_msg = response.json() if response else "Connection error"
                                st.error(f"❌ {platform_data['platform']}: Failed - {error_msg}")
                            
                            progress_bar.progress((idx + 1) / len(platforms_to_post))
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if error_count == 0:
                            st.balloons()
                            st.success(f"🎉 Successfully posted to all {success_count} platform(s)!")
                        else:
                            st.warning(f"⚠️ Posted to {success_count} platform(s), {error_count} failed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Platform selection with modern cards
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>🌐 Select Your Platforms</h3>
            <p style='color: #666; margin: 0;'>Choose which platforms to post to</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        enable_instagram = st.checkbox("📷 **Instagram**", value=False, key="enable_ig")
    with col2:
        enable_linkedin = st.checkbox("💼 **LinkedIn**", value=False, key="enable_li")
    with col3:
        enable_facebook = st.checkbox("👥 **Facebook**", value=False, key="enable_fb")
    with col4:
        enable_twitter = st.checkbox("🐦 **Twitter**", value=False, key="enable_tw")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Platform-specific configurations
    platforms_config = []
    
    # Instagram Configuration - FIXED
    if enable_instagram:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #bc1888;'>📷 Instagram Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # FIXED: Use session state directly through key parameter
                ig_account_id = st.text_input(
                    "🆔 Instagram Account ID",
                    key="ig_account_id",
                    placeholder="Enter your Instagram account ID"
                )
                
                if ig_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'ig_content_value' not in st.session_state:
                    st.session_state.ig_content_value = ""
                if 'ig_refresh_counter' not in st.session_state:
                    st.session_state.ig_refresh_counter = 0
                
                ig_content = st.text_area(
                    "💬 Caption",
                    value=st.session_state.ig_content_value,
                    height=100,
                    key=f"ig_content_area_{st.session_state.ig_refresh_counter}",
                    placeholder="Your Instagram caption with hashtags..."
                )
                if ig_content != st.session_state.ig_content_value:
                    st.session_state.ig_content_value = ig_content
            
            with col2:
                use_master_ig = st.button("📋 Use Master", key="ig_use_master_btn", use_container_width=True)
                
                if use_master_ig:
                    st.session_state.ig_content_value = st.session_state.master_content
                    if 'ig_refresh_counter' not in st.session_state:
                        st.session_state.ig_refresh_counter = 0
                    st.session_state.ig_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule = st.checkbox("Use master schedule", value=True, key="ig_master_sched")
                
                if not use_master_schedule:
                    ig_date = st.date_input("Date", value=default_date, key="ig_schedule_date")
                    ig_time = st.time_input("Time (PDT)", value=default_date.time(), key="ig_schedule_time")
                    ig_datetime = datetime.combine(ig_date, ig_time)
                    ig_datetime_pdt = pdt.localize(ig_datetime)
                    ig_schedule = ig_datetime_pdt.isoformat()
                else:
                    ig_schedule = st.session_state.master_schedule
            
            if ig_account_id:
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Instagram",
                    "accountId": ig_account_id,
                    "content": st.session_state.ig_content_value,
                    "schedule": ig_schedule,
                    "mediaItems": media_items
                })
    
    # LinkedIn Configuration - FIXED
    if enable_linkedin:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #0077b5;'>💼 LinkedIn Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # FIXED: Use session state directly through key parameter
                li_account_id = st.text_input(
                    "🆔 LinkedIn Account ID",
                    key="li_account_id",
                    placeholder="Enter your LinkedIn account ID"
                )
                
                if li_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'li_content_value' not in st.session_state:
                    st.session_state.li_content_value = ""
                if 'li_refresh_counter' not in st.session_state:
                    st.session_state.li_refresh_counter = 0
                
                li_content = st.text_area(
                    "💬 Post Content",
                    value=st.session_state.li_content_value,
                    height=100,
                    key=f"li_content_area_{st.session_state.li_refresh_counter}",
                    placeholder="Your professional LinkedIn post..."
                )
                if li_content != st.session_state.li_content_value:
                    st.session_state.li_content_value = li_content
            
            with col2:
                use_master_li = st.button("📋 Use Master", key="li_use_master_btn", use_container_width=True)
                
                if use_master_li:
                    st.session_state.li_content_value = st.session_state.master_content
                    if 'li_refresh_counter' not in st.session_state:
                        st.session_state.li_refresh_counter = 0
                    st.session_state.li_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_li = st.checkbox("Use master schedule", value=True, key="li_master_sched")
                
                if not use_master_schedule_li:
                    li_date = st.date_input("Date", value=default_date, key="li_schedule_date")
                    li_time = st.time_input("Time (PDT)", value=default_date.time(), key="li_schedule_time")
                    li_datetime = datetime.combine(li_date, li_time)
                    li_datetime_pdt = pdt.localize(li_datetime)
                    li_schedule = li_datetime_pdt.isoformat()
                else:
                    li_schedule = st.session_state.master_schedule
            
            if li_account_id:
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "LinkedIn",
                    "accountId": li_account_id,
                    "content": st.session_state.li_content_value,
                    "schedule": li_schedule,
                    "mediaItems": media_items
                })
    
    # Facebook Configuration - FIXED
    if enable_facebook:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #1877f2 0%, #0c63d4 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #1877f2;'>👥 Facebook Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # FIXED: Use session state directly through key parameter
                fb_account_id = st.text_input(
                    "🆔 Facebook Account ID",
                    key="fb_account_id",
                    placeholder="Enter your Facebook account ID"
                )
                
                if fb_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'fb_content_value' not in st.session_state:
                    st.session_state.fb_content_value = ""
                if 'fb_refresh_counter' not in st.session_state:
                    st.session_state.fb_refresh_counter = 0
                
                fb_content = st.text_area(
                    "💬 Post Content",
                    value=st.session_state.fb_content_value,
                    height=100,
                    key=f"fb_content_area_{st.session_state.fb_refresh_counter}",
                    placeholder="Your Facebook post..."
                )
                if fb_content != st.session_state.fb_content_value:
                    st.session_state.fb_content_value = fb_content
            
            with col2:
                use_master_fb = st.button("📋 Use Master", key="fb_use_master_btn", use_container_width=True)
                
                if use_master_fb:
                    st.session_state.fb_content_value = st.session_state.master_content
                    if 'fb_refresh_counter' not in st.session_state:
                        st.session_state.fb_refresh_counter = 0
                    st.session_state.fb_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_fb = st.checkbox("Use master schedule", value=True, key="fb_master_sched")
                
                if not use_master_schedule_fb:
                    fb_date = st.date_input("Date", value=default_date, key="fb_schedule_date")
                    fb_time = st.time_input("Time (PDT)", value=default_date.time(), key="fb_schedule_time")
                    fb_datetime = datetime.combine(fb_date, fb_time)
                    fb_datetime_pdt = pdt.localize(fb_datetime)
                    fb_schedule = fb_datetime_pdt.isoformat()
                else:
                    fb_schedule = st.session_state.master_schedule
            
            if fb_account_id:
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Facebook",
                    "accountId": fb_account_id,
                    "content": st.session_state.fb_content_value,
                    "schedule": fb_schedule,
                    "mediaItems": media_items
                })
    
    # Twitter Configuration - FIXED
    if enable_twitter:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #1DA1F2 0%, #0c85d0 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #1DA1F2;'>🐦 Twitter Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # FIXED: Use session state directly through key parameter
                tw_account_id = st.text_input(
                    "🆔 Twitter Account ID",
                    key="tw_account_id",
                    placeholder="Enter your Twitter account ID"
                )
                
                if tw_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'tw_content_value' not in st.session_state:
                    st.session_state.tw_content_value = ""
                if 'tw_refresh_counter' not in st.session_state:
                    st.session_state.tw_refresh_counter = 0
                
                tw_content = st.text_area(
                    "💬 Tweet Content",
                    value=st.session_state.tw_content_value,
                    height=100,
                    key=f"tw_content_area_{st.session_state.tw_refresh_counter}",
                    placeholder="Your tweet (max 280 characters)...",
                    max_chars=280
                )
                if tw_content != st.session_state.tw_content_value:
                    st.session_state.tw_content_value = tw_content
                
                char_count = len(tw_content)
                if char_count > 280:
                    st.error(f"⚠️ Tweet is {char_count - 280} characters over the limit!")
                elif char_count > 250:
                    st.warning(f"⚡ {280 - char_count} characters remaining")
                else:
                    st.info(f"✍️ {char_count}/280 characters used")
            
            with col2:
                use_master_tw = st.button("📋 Use Master", key="tw_use_master_btn", use_container_width=True)
                
                if use_master_tw:
                    st.session_state.tw_content_value = st.session_state.master_content
                    if 'tw_refresh_counter' not in st.session_state:
                        st.session_state.tw_refresh_counter = 0
                    st.session_state.tw_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_tw = st.checkbox("Use master schedule", value=True, key="tw_master_sched")
                
                if not use_master_schedule_tw:
                    tw_date = st.date_input("Date", value=default_date, key="tw_schedule_date")
                    tw_time = st.time_input("Time (PDT)", value=default_date.time(), key="tw_schedule_time")
                    tw_datetime = datetime.combine(tw_date, tw_time)
                    tw_datetime_pdt = pdt.localize(tw_datetime)
                    tw_schedule = tw_datetime_pdt.isoformat()
                else:
                    tw_schedule = st.session_state.master_schedule
            
            if tw_account_id:
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Twitter",
                    "accountId": tw_account_id,
                    "content": st.session_state.tw_content_value,
                    "schedule": tw_schedule,
                    "mediaItems": media_items
                })
    
    # Preview and Submit Section
    if platforms_config:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 2rem 0;'>
                <h3 style='margin-top: 0;'>👀 Preview Your Posts</h3>
                <p style='color: #666; margin: 0;'>Review your content before scheduling</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show preview for each platform
        for platform_data in platforms_config:
            platform_colors = {
                "Instagram": "linear-gradient(135deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%)",
                "LinkedIn": "linear-gradient(135deg, #0077b5 0%, #00a0dc 100%)",
                "Facebook": "linear-gradient(135deg, #1877f2 0%, #0c63d4 100%)",
                "Twitter": "linear-gradient(135deg, #1DA1F2 0%, #0c85d0 100%)"
            }
            
            platform_icons = {
                "Instagram": "📷",
                "LinkedIn": "💼",
                "Facebook": "👥",
                "Twitter": "🐦"
            }
            
            st.markdown(f"""
                <div style='background: {platform_colors.get(platform_data["platform"], "#667eea")}; 
                            padding: 0.1rem; border-radius: 12px; margin: 1rem 0;'>
                    <div style='background: white; padding: 1.5rem; border-radius: 11px;'>
                        <h4 style='margin: 0; color: #333;'>{platform_icons.get(platform_data["platform"], "📱")} {platform_data["platform"]}</h4>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**📝 Content:**")
                if platform_data['content']:
                    st.info(platform_data['content'])
                else:
                    st.warning("_No content provided_")
                
                if platform_data['mediaItems']:
                    st.success(f"📷 {len(platform_data['mediaItems'])} image(s) attached")
            
            with col2:
                st.markdown("**🆔 Account ID:**")
                st.code(platform_data['accountId'], language=None)
                
                st.markdown("**📅 Scheduled for:**")
                schedule_time = datetime.fromisoformat(platform_data['schedule'])
                st.write(schedule_time.strftime("%B %d, %Y"))
                st.write(schedule_time.strftime("%I:%M %p PDT"))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Final API payload preview
        with st.expander("🔍 View Technical Details (API Payload)", expanded=False):
            for platform_data in platforms_config:
                payload = build_post_payload(
                    content=platform_data['content'],
                    scheduled_time=platform_data['schedule'],
                    timezone="America/Los_Angeles",
                    platforms_config=[{
                        "accountId": platform_data['accountId'],
                        "mediaItems": platform_data['mediaItems']
                    }]
                )
                
                st.markdown(f"**{platform_data['platform']} API Payload:**")
                st.json(payload)
                st.markdown("---")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit button with modern styling
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; text-align: center;'>
                <h3 style='margin-top: 0;'>🚀 Ready to Launch?</h3>
                <p style='color: #666; margin: 0;'>Schedule your posts across all selected platforms</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Schedule Posts to All Platforms", type="primary", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("❌ Please enter your API key in the sidebar!")
                else:
                    with st.spinner("📤 Scheduling your posts across platforms..."):
                        success_count = 0
                        error_count = 0
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, platform_data in enumerate(platforms_config):
                            status_text.text(f"Posting to {platform_data['platform']}...")
                            
                            payload = build_post_payload(
                                content=platform_data['content'],
                                scheduled_time=platform_data['schedule'],
                                timezone="America/Los_Angeles",
                                platforms_config=[{
                                    "accountId": platform_data['accountId'],
                                    "mediaItems": platform_data['mediaItems']
                                }]
                            )
                            
                            response = send_post_to_api(st.session_state.api_key, payload)
                            
                            if response and response.status_code in [200, 201]:
                                success_count += 1
                                st.success(f"✅ {platform_data['platform']}: Post scheduled successfully!")
                            else:
                                error_count += 1
                                error_msg = response.json() if response else "Connection error"
                                st.error(f"❌ {platform_data['platform']}: Failed to schedule post")
                                with st.expander("View Error Details"):
                                    st.error(f"Error: {error_msg}")
                            
                            progress_bar.progress((idx + 1) / len(platforms_config))
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if error_count == 0:
                            st.balloons()
                            st.markdown("""
                                <div style='background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                            padding: 2rem; border-radius: 16px; text-align: center;'>
                                    <h2 style='margin: 0; color: #155724;'>🎉 Success!</h2>
                                    <p style='color: #155724; margin: 0.5rem 0 0 0;'>All {success_count} posts scheduled successfully!</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                                            padding: 2rem; border-radius: 16px; text-align: center;'>
                                    <h3 style='margin: 0; color: #856404;'>⚠️ Partial Success</h3>
                                    <p style='color: #856404; margin: 0.5rem 0 0 0;'>{success_count} successful, {error_count} failed</p>
                                </div>
                            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
                        padding: 3rem; border-radius: 16px; text-align: center; margin: 3rem 0;'>
                <h3 style='margin: 0; color: #0c5460;'>👆 Select at least one platform to get started</h3>
                <p style='color: #0c5460; margin: 0.5rem 0 0 0;'>Check the boxes above to enable platforms</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: CREATE SHORT FORM VIDEO POST
# ============================================================================

with tab4:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎬 Short Form Video Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>TikTok, Reels, YouTube Shorts - Coming Soon!</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
            <h2 style='margin: 0; color: #667eea;'>🚧 Feature In Development</h2>
            <p style='color: #666; margin: 1rem 0 0 0; font-size: 1.1rem;'>We're working hard to bring you the best short-form video posting experience!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px; text-align: center; min-height: 200px;'>
                    <h2 style='font-size: 3rem; margin: 0;'>📱</h2>
                    <h3 style='margin: 1rem 0; color: #667eea;'>TikTok</h3>
                    <p style='color: #666; margin: 0;'>Upload and schedule TikTok videos with captions and hashtags</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f09433 0%, #bc1888 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px; text-align: center; min-height: 200px;'>
                    <h2 style='font-size: 3rem; margin: 0;'>🎥</h2>
                    <h3 style='margin: 1rem 0; color: #bc1888;'>Instagram Reels</h3>
                    <p style='color: #666; margin: 0;'>Create and post engaging Instagram Reels instantly</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px; text-align: center; min-height: 200px;'>
                    <h2 style='font-size: 3rem; margin: 0;'>▶️</h2>
                    <h3 style='margin: 1rem 0; color: #FF0000;'>YouTube Shorts</h3>
                    <p style='color: #666; margin: 0;'>Upload vertical videos as YouTube Shorts</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Planned features
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 2rem 0;'>
            <h3 style='margin-top: 0; text-align: center;'>🎯 Planned Features</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📤 Upload & Management
        - 📹 Video file upload (MP4, MOV, etc.)
        - ✂️ Built-in video trimming
        - 🖼️ Custom thumbnail selection
        - 📏 Automatic aspect ratio detection
        - 💾 Draft saving
        """)
        
        st.markdown("""
        ### 🎨 Customization
        - 📝 Caption & hashtag editor
        - 🎵 Background music library
        - 🎭 Filter & effects
        - 📍 Location tagging
        - 👥 Collaborator tagging
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Analytics & Insights
        - 📈 Cross-platform analytics
        - ⏰ Best time to post suggestions
        - 🎯 Engagement predictions
        - 📉 Performance tracking
        - 🔄 A/B testing
        """)
        
        st.markdown("""
        ### 🚀 Advanced Features
        - 📅 Bulk scheduling
        - 🔄 Auto-repost to multiple platforms
        - 📱 Mobile app integration
        - 🤖 AI caption generator
        - 🎬 Video templates
        """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; color: white;'>
            <h2 style='margin: 0 0 1rem 0; color: white;'>Want Early Access?</h2>
            <p style='margin: 0 0 1.5rem 0; font-size: 1.1rem;'>Be the first to know when short-form video posting goes live!</p>
            <a href='mailto:miki@getlate.dev?subject=Early Access Request' 
               style='display: inline-block; background: white; color: #667eea; padding: 12px 32px; 
                      border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s;'>
                📧 Request Early Access
            </a>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
            padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;'>
    <p style='margin: 0; color: #666; font-size: 0.9rem;'>
        Made with ❤️ for content creators | 
        <a href='https://getlate.dev' target='_blank' style='color: #667eea; text-decoration: none; font-weight: 600;'>
            Powered by GetLate
        </a>
    </p>
    <p style='margin: 0.5rem 0 0 0; color: #999; font-size: 0.8rem;'>
        © 2025 Content Posting Automations | All rights reserved
    </p>
</div>
""", unsafe_allow_html=True)































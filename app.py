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
# CONFIGURATION - INPUT YOUR API KEY AND ACCOUNT IDs HERE
# ============================================================================
# TODO: Replace these dummy values with your actual credentials
FIXED_API_KEY = "sk_e49ce1a9dacec6a32b40c405d521a41db3a2d614bbb0e32111a9f39acef48c2b"  # Replace with your actual GetLate API key

# Tab 3 (Multi-Platform Post Creator) Account IDs
INSTAGRAM_ACCOUNT_ID = "69105863ef0527b8b3cfe9de"  # Replace with your Instagram account ID
LINKEDIN_ACCOUNT_ID = "123456"   # Replace with your LinkedIn account ID
FACEBOOK_ACCOUNT_ID = "123456"   # Replace with your Facebook account ID
TWITTER_ACCOUNT_ID = "123456"    # Replace with your Twitter account ID

# Tab 4 (Short Form Video Creator) Account IDs
YOUTUBE_ACCOUNT_ID = "69105863ef0527b8b3cfe9de"           # Replace with your YouTube account ID
INSTAGRAM_VIDEO_ACCOUNT_ID = "69116f39ef0527b8b3cfea5a"  # Replace with your Instagram account ID for videos
TIKTOK_ACCOUNT_ID = "123456"           # Replace with your TikTok account ID
FACEBOOK_VIDEO_ACCOUNT_ID = "123456"   # Replace with your Facebook account ID for videos

# ============================================================================
# PASSWORD PROTECTION - ENHANCED VERSION
# ============================================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256("RenaPostTool81".encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        st.markdown("""
            <style>
                /* Hide Streamlit defaults */
                #MainMenu {visibility: hidden !important;}
                footer {visibility: hidden !important;}
                header {visibility: hidden !important;}
                .stDeployButton {visibility: hidden !important;}
                
                /* Background gradient */
                .stApp {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                }
                .main {
                    background: transparent !important;
                    padding: 0 !important;
                }
                .main .block-container {
                    padding: 2rem 1rem !important; 
                    padding-top: 8rem !important;
                    max-width: 100% !important;
                    margin: 0 !important;
                }
                
                /* CRITICAL: Slide-in keyframes */
                @keyframes slideInUp {
                    0% {
                        opacity: 0;
                        transform: translateY(60px) scale(0.95);
                    }
                    100% {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                    }
                }
                
                @keyframes twinkle {
                    0%, 100% { opacity: 0.2; transform: scale(0.8); }
                    50% { opacity: 1; transform: scale(1.2); }
                }
                
                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-10px); }
                }
                
                /* Stars */
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
                    box-shadow: 0 0 6px rgba(255,255,255,0.9);
                }
                .star:nth-child(odd) { animation: twinkle 2s infinite, float 4s ease-in-out infinite; }
                .star:nth-child(even) { animation: twinkle 3s infinite 0.5s, float 5s ease-in-out infinite; }
                
                /* Login card with slide-in animation */
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
                    animation: slideInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                
                .login-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
                }
                
                .login-title {
                    color: white;
                    font-size: 2.5rem;
                    font-weight: 800;
                    text-align: center;
                    margin: 0 0 0.8rem 0;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                    letter-spacing: -0.03em;
                    line-height: 1.2;
                    background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
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
                
                /* Password input styling */
                .stTextInput > div > div > input {
                    background: rgba(255, 255, 255, 0.9) !important;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 255, 255, 0.4) !important;
                    border-radius: 14px !important;
                    color: #2d3748 !important;
                    padding: 16px 20px !important;
                    font-size: 1rem !important;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
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
                
                .stTextInput > div > div > input::placeholder {
                    color: rgba(45, 55, 72, 0.5) !important;
                }
                
                .stTextInput > div > div > input:focus {
                    border-color: #667eea !important;
                    background: white !important;
                    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
                    outline: none !important;
                    transform: scale(1.02);
                }
                
                .stTextInput > label {
                    display: none !important;
                }
                
                /* Button styling */
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
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    width: 340px !important;
                    letter-spacing: 0.5px !important;
                }
                
                .stButton > button:hover {
                    background: white !important;
                    border-color: #667eea !important;
                    transform: translateY(-2px) scale(1.02) !important;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
                }
                
                .stButton > button:active {
                    transform: translateY(0) scale(0.98) !important;
                }
                
                .login-form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
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
        
        # Centered login card
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("""
                <div class="login-card">
                    <h1 class="login-title">All-in-One Content Tool</h1>
                    <p class="login-subtitle">Enter your password to access the tool</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
            
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            password_input = st.text_input(
                "Password", 
                type="password",
                key="password",
                placeholder="Enter your password...",
                label_visibility="collapsed"
            )
            
            if st.button("🔓 LOGIN", use_container_width=True, type="primary"):
                if password_input:
                    if hashlib.sha256(password_input.encode()).hexdigest() == hashlib.sha256("RenaPostTool81".encode()).hexdigest():
                        st.session_state["password_correct"] = True
                        st.balloons()
                        st.rerun()
                    else:
                        st.session_state["password_correct"] = False
                        st.error("❌ Incorrect password. Please try again.")
                else:
                    st.warning("⚠️ Please enter a password")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("""
                <div class="login-footer">
                    🔐 Secure access • Content Posting Automations
                </div>
            """, unsafe_allow_html=True)
        
        return False
        
    elif not st.session_state["password_correct"]:
        st.error("❌ Incorrect password. Please try again.")
        del st.session_state["password_correct"]
        st.rerun()
        return False
    else:
        return True
# ============================================================================
# CTA IMAGE CREATION FUNCTION (Add this near the top with other functions)
# ============================================================================

def create_cta_podcast_image(bg_color, bg_image, cta_label, cta_box_color, guest_name, episode_title):
    """Create CTA podcast image matching the template"""
    
    # Image dimensions
    POST_SIZE = 1080
    
    # Create base image
    if bg_image:
        # Use uploaded background image
        base_img = Image.open(bg_image)
        base_img = resize_image_to_exact(base_img, POST_SIZE, POST_SIZE)
    else:
        # Use solid color
        base_img = Image.new('RGB', (POST_SIZE, POST_SIZE), color=bg_color)
    
    # Create drawing context
    draw = ImageDraw.Draw(base_img)
    
    # --- CTA Label Box (Top-Left) ---
    cta_box_padding = 20
    cta_font_size = 80
    cta_font = get_font(cta_font_size, bold=True)
    
    # Calculate CTA box dimensions
    cta_bbox = draw.textbbox((0, 0), cta_label, font=cta_font)
    cta_text_width = cta_bbox[2] - cta_bbox[0]
    cta_text_height = cta_bbox[3] - cta_bbox[1]
    
    cta_box_width = cta_text_width + (cta_box_padding * 2)
    cta_box_height = cta_text_height + (cta_box_padding * 2)
    
    # Draw CTA box
    cta_box_pos = (80, 120)
    draw.rectangle(
        [cta_box_pos[0], cta_box_pos[1], 
         cta_box_pos[0] + cta_box_width, cta_box_pos[1] + cta_box_height],
        fill=cta_box_color
    )
    
    # Draw CTA text
    cta_text_pos = (cta_box_pos[0] + cta_box_padding, cta_box_pos[1] + cta_box_padding)
    draw.text(cta_text_pos, cta_label, fill='#1A2238', font=cta_font)
    
    # --- Main Message Text ---
    main_text = f'Listen to the full conversation with special guest {guest_name} on the "Rena Malik, MD Podcast"'
    main_font_size = 42
    main_font = get_font(main_font_size, bold=False)
    
    # Wrap text
    max_width = POST_SIZE - 160
    wrapped_main_text = wrap_text(main_text, main_font, max_width)
    
    # Position main text (centered vertically, left-aligned)
    main_text_x = 80
    main_text_y = 450
    
    draw.multiline_text(
        (main_text_x, main_text_y),
        wrapped_main_text,
        fill='#1A2238',
        font=main_font,
        spacing=10
    )
    
    # --- Episode Info (Bottom-Left) ---
    episode_text = f"🎙️Episode: {episode_title}"
    episode_font_size = 32
    episode_font = get_font(episode_font_size, bold=False)
    
    episode_pos = (80, POST_SIZE - 200)
    draw.text(episode_pos, episode_text, fill='#1A2238', font=episode_font)
    
    # --- Podcast Cover (Bottom-Right) - LOAD FROM GOOGLE DRIVE ---
    try:
        # Your podcast cover Google Drive link
        PODCAST_COVER_URL = "https://drive.google.com/uc?export=download&id=1Bb2Kc6Y_exps6NV-s73l3DFGV8Nj2Wj3"
        
        # Download image from Google Drive
        response = requests.get(PODCAST_COVER_URL)
        if response.status_code == 200:
            cover_img = Image.open(BytesIO(response.content))
            cover_size = 250
            cover_img = resize_image_to_exact(cover_img, cover_size, cover_size)
            
            # Position in bottom-right
            cover_x = POST_SIZE - cover_size - 60
            cover_y = POST_SIZE - cover_size - 60
            
            # Paste cover (handle transparency)
            if cover_img.mode == 'RGBA':
                base_img.paste(cover_img, (cover_x, cover_y), cover_img)
            else:
                base_img.paste(cover_img, (cover_x, cover_y))
        else:
            st.warning("⚠️ Could not load podcast cover from Google Drive")
            
    except Exception as e:
        st.warning(f"⚠️ Could not add podcast cover: {str(e)}")
    
    return base_img

# ============================================================================
# YOUTUBE TO INSTAGRAM POST FUNCTIONS
# ============================================================================
def get_font(size, bold=False):
    """Get Work Sans SemiBold font or fallback to default"""
    try:
        font_paths = [
            "WorkSans-SemiBold.ttf" if not bold else "WorkSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "arial.ttf"
        ]
        
        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
                
        return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def create_posts_from_uploads(uploaded_files, image_captions, guest_name="", logo_file=None):
    """Create Instagram posts from uploaded images with individual captions per image"""
    
    instagram_posts = []
    
    images = []
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        images.append(img)
    
    # Process images in pairs
    for i in range(0, len(images), 2):
        post_images = images[i:i+2]
        
        # Get captions for each image in the pair
        if len(post_images) == 2:
            top_caption = image_captions[i] if i < len(image_captions) else ""
            bottom_caption = image_captions[i+1] if (i+1) < len(image_captions) else ""
            captions = [top_caption, bottom_caption]
        else:
            captions = [image_captions[i] if i < len(image_captions) else ""]
        
        instagram_post = create_single_instagram_post(post_images, captions)
        instagram_posts.append(instagram_post)
    
    # Add promotional post at the end
    if guest_name.strip():
        promo_post = create_promotional_post(guest_name, logo_file)
        instagram_posts.append(promo_post)
    
    return instagram_posts

def create_single_instagram_post(images, captions):
    """Create a single Instagram post from 1 or 2 images with individual captions"""
    
    POST_SIZE = 1080
    
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='white')
    
    if len(images) == 2:
        top_img = images[0]
        bottom_img = images[1]
        
        img_height = POST_SIZE // 2
        
        top_img = resize_image_to_exact(top_img, POST_SIZE, img_height)
        bottom_img = resize_image_to_exact(bottom_img, POST_SIZE, img_height)
        
        # Use individual captions instead of splitting
        if len(captions) >= 1 and captions[0].strip():
            top_img = add_text_overlay(top_img, captions[0])
        if len(captions) >= 2 and captions[1].strip():
            bottom_img = add_text_overlay(bottom_img, captions[1])
        
        post.paste(top_img, (0, 0))
        post.paste(bottom_img, (0, POST_SIZE // 2))
        
    else:
        img = images[0]
        img = resize_image_to_exact(img, POST_SIZE, POST_SIZE)
        
        if len(captions) >= 1 and captions[0].strip():
            img = add_text_overlay(img, captions[0])
        
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
    initial_sidebar_state="expanded"
)

# Check password first
if not check_password():
    st.stop()

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
    
    /* Main Container */
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
    
    /* Force tab text colors */
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
    
    /* Sidebar Styling */
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

# Initialize session state
if 'master_content' not in st.session_state:
    st.session_state.master_content = ""
if 'master_schedule' not in st.session_state:
    st.session_state.master_schedule = None
# Tab 1 Instagram posting
if 'generated_ig_posts' not in st.session_state:
    st.session_state.generated_ig_posts = None
if 'show_ig_posting' not in st.session_state:
    st.session_state.show_ig_posting = False
if 'post_texts_for_ig' not in st.session_state:
    st.session_state.post_texts_for_ig = []

# API Key display in sidebar (read-only)
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Display API key as read-only
    st.markdown("**🔑 GetLate API Key**")
    st.text_input(
        "API Key", 
        value=FIXED_API_KEY,
        disabled=True,
        label_visibility="collapsed",
        key="display_api_key"
    )
    st.success("✅ API Key Configured")
    
    st.markdown("---")
    st.markdown("### 📚 Resources")
    st.markdown("🔗 [GetLate Dashboard](https://getlate.dev/dashboard)")
    st.markdown("📖 [API Documentation](https://getlate.dev/docs)")
    st.markdown("💬 [Support](mailto:miki@getlate.dev)")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.info("🟢 API Connected")
    
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
    
    # YouTube Video Embed Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(255, 0, 0, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>🎥 Watch & Screenshot YouTube Video</h3>
            <p style='color: #666; margin: 0.5rem 0 0 0;'>Paste a YouTube link to watch and take screenshots directly</p>
        </div>
    """, unsafe_allow_html=True)
    
    youtube_url = st.text_input(
        "🔗 Paste YouTube URL here",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ or https://youtu.be/dQw4w9WgXcQ",
        help="Paste any YouTube video link"
    )
    
    if youtube_url:
        # Extract video ID from URL
        video_id = None
        
        if "youtube.com/watch?v=" in youtube_url:
            video_id = youtube_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/embed/" in youtube_url:
            video_id = youtube_url.split("embed/")[1].split("?")[0]
        
        if video_id:
            st.markdown("""
                <div style='background: black; padding: 1rem; border-radius: 12px; margin: 1rem 0;'>
            """, unsafe_allow_html=True)
            
            # Embed YouTube video
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Screenshot instructions
            with st.expander("📸 How to Take Screenshots from the Video", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **⌨️ Keyboard Shortcuts:**
                    - **Windows:** `Win + Shift + S` or `PrtScn`
                    - **Mac:** `Cmd + Shift + 4`
                    - **Chrome Extension:** Use Awesome Screenshot
                    """)
                with col2:
                    st.markdown("""
                    **💡 Pro Tips:**
                    - ⏸️ Pause at key moments
                    - 🖼️ Take screenshots of interesting frames
                    - 📥 Upload them below to create posts
                    - 🎯 Aim for 2 screenshots per post
                    """)
            
            st.info("💡 **Tip:** Play the video above, pause at moments you want to capture, take screenshots using your keyboard shortcuts, then upload them below!")
        else:
            st.warning("⚠️ Invalid YouTube URL. Please enter a valid YouTube link.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
        
        # Text input section with individual captions per image
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
                <h3 style='margin-top: 0;'>✍️ Add Captions to Your Images</h3>
                <p style='color: #666; margin: 0.5rem 0 0 0;'>Each image gets its own caption overlay at the bottom</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state for image captions
        if 'tab1_image_captions' not in st.session_state:
            st.session_state.tab1_image_captions = {}
        
        # Create individual caption textboxes for each image
        image_captions = []
        for img_idx in range(len(uploaded_files)):
            # Calculate which post this image belongs to
            post_number = (img_idx // 2) + 1
            image_position = "Top" if img_idx % 2 == 0 else "Bottom"
            
            # Calculate pair info
            if img_idx % 2 == 0 and img_idx + 1 < len(uploaded_files):
                pair_info = f"(Pairs with Image #{img_idx + 2})"
            elif img_idx % 2 == 1:
                pair_info = f"(Pairs with Image #{img_idx})"
            else:
                pair_info = "(Single image)"
            
            st.markdown(f"**Image #{img_idx + 1}** - Post {post_number} ({image_position}) {pair_info}")
            
            caption_key = f"img_caption_{img_idx}"
            caption_value = st.session_state.tab1_image_captions.get(caption_key, "")
            
            caption = st.text_area(
                f"Caption for Image #{img_idx + 1}",
                value=caption_value,
                height=80,
                placeholder=f"Write caption for Image #{img_idx + 1}...",
                key=caption_key,
                help=f"This caption will be overlaid on Image #{img_idx + 1} ({image_position} of Post {post_number})",
                label_visibility="collapsed"
            )
            
            # Update session state
            st.session_state.tab1_image_captions[caption_key] = caption
            image_captions.append(caption)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Customization options
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
                <h3 style='margin-top: 0;'>🎨 Customization Options</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            include_originals = st.checkbox("📦 Include originals in ZIP", value=True)
        with col2:
            guest_name = st.text_input("👤 Guest name (optional)", placeholder="Dr. Jane Smith", help="If provided, a promotional post will be added at the end")
        with col3:
            logo_file = st.file_uploader("🎭 Podcast logo (optional)", type=['png', 'jpg', 'jpeg'], help="Logo for the promotional post")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create and Download buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎨 ✨ Generate Instagram Posts", type="primary", use_container_width=True):
                with st.spinner("✨ Creating your beautiful Instagram posts..."):
                    instagram_posts = create_posts_from_uploads(
                        uploaded_files, 
                        image_captions,
                        guest_name, 
                        logo_file
                    )
                    
                    # Store in session state
                    st.session_state.generated_ig_posts = instagram_posts
                    st.session_state.post_captions = image_captions
                    
                    st.success(f"🎉 Successfully created {len(instagram_posts)} Instagram posts!")
                    
                    # Show preview in a beautiful grid
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 👀 Preview Your Amazing Posts")
                    cols = st.columns(3)
                    for i, post_img in enumerate(instagram_posts):
                        with cols[i % 3]:
                            st.image(post_img, caption=f"Post {i+1}", use_container_width=True)
                            # Show caption if it's not the promo post
                            if i < len(image_captions):
                                # Show captions for the two images in this post
                                img_start = i * 2
                                img_end = min(img_start + 2, len(image_captions))
                                if img_start < len(image_captions):
                                    with st.expander(f"📝 Captions for Post {i+1}"):
                                        if img_start < len(image_captions) and image_captions[img_start]:
                                            st.write(f"**Top Image:** {image_captions[img_start]}")
                                        if img_start + 1 < len(image_captions) and image_captions[img_start + 1]:
                                            st.write(f"**Bottom Image:** {image_captions[img_start + 1]}")
                            elif i == len(instagram_posts) - 1 and guest_name:
                                with st.expander(f"📢 Promotional Post"):
                                    st.write(f"Listen to the full conversation with {guest_name}")
                    
                    # Download section
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                                    padding: 2rem; border-radius: 16px; text-align: center;'>
                            <h3 style='margin-top: 0;'>📥 Download Your Posts</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Individual downloads
                    st.markdown("### 📄 Download Individual Posts")
                    cols = st.columns(min(len(instagram_posts), 3))
                    for i, post_img in enumerate(instagram_posts):
                        with cols[i % 3]:
                            # Convert PIL Image to bytes for download
                            img_bytes = BytesIO()
                            post_img.save(img_bytes, format='JPEG', quality=95)
                            img_bytes.seek(0)
                            
                            st.download_button(
                                label=f"⬇️ Post {i+1}",
                                data=img_bytes,
                                file_name=f"instagram_post_{i+1}.jpg",
                                mime="image/jpeg",
                                use_container_width=True,
                                key=f"download_post_{i}"
                            )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Download all as ZIP
                    st.markdown("### 📦 Download All Posts")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        original_imgs = uploaded_files if include_originals else None
                        zip_data = create_zip_from_posts(instagram_posts, original_imgs)
                        
                        st.download_button(
                            label="⬇️ Download All Posts (ZIP)",
                            data=zip_data,
                            file_name=f"instagram_posts_{len(instagram_posts)}.zip",
                            mime="application/zip",
                            use_container_width=True,
                            type="primary"
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Info box
                    promo_text = f"+ 1 promotional post for {guest_name}" if guest_name else ""
                    st.info(f"""
                    **📦 Your download includes:**
                    - ✅ {num_posts} Instagram-ready posts (1080x1080px) {promo_text}
                    - ✅ Text overlays automatically positioned at bottom of images
                    - ✅ Individual captions on each image
                    - ✅ Optimized for Instagram carousel format
                    {"- ✅ Original screenshots included" if include_originals else ""}
                    
                    **💡 Next steps:**
                    1. Download your posts
                    2. Open Instagram app
                    3. Create new post → Select multiple images
                    4. Upload in order and add your caption
                    5. Share with your audience! 🚀
                    """)
    
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
                        padding: 3rem; border-radius: 16px; text-align: center; margin: 3rem 0;'>
                <h3 style='margin: 0; color: #0c5460;'>👆 Paste a YouTube link above or upload screenshots to get started</h3>
                <p style='color: #0c5460; margin: 0.5rem 0 0 0;'>Watch the video and take screenshots, or upload existing screenshots</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: CTA PODCAST CONTENT CREATION
# ============================================================================

with tab2:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎙️ CTA Podcast Content Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>Create engaging call-to-action posts for your podcast episodes</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for tab 2
    if 'tab2_cta_image' not in st.session_state:
        st.session_state.tab2_cta_image = None
    
    # Two column layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;'>
                <h3 style='margin-top: 0;'>🎨 Customize Your CTA</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Background Options
        st.markdown("### 🖼️ Background Settings")
        background_option = st.radio(
            "Choose background type",
            ["Solid Color", "Upload Image"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if background_option == "Solid Color":
            bg_color = st.color_picker("Background Color", value="#E8D58A", help="Pick your background color")
            bg_image = None
        else:
            bg_color = None
            bg_image = st.file_uploader("Upload Background Image", type=['png', 'jpg', 'jpeg'], help="Upload a custom background image")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Text Customization
        st.markdown("### ✍️ Text Content")
        
        cta_label = st.text_input(
            "CTA Label",
            value="[CTA]",
            help="The label in the top-left box"
        )
        
        cta_box_color = st.color_picker("CTA Box Color", value="#9DB4E8", help="Background color for CTA label box")
        
        guest_name = st.text_input(
            "Guest Name",
            value="[Guest]",
            placeholder="Dr. Jane Smith",
            help="Name of your podcast guest"
        )
        
        episode_title = st.text_input(
            "Episode Title",
            value="[Episode Title]",
            placeholder="Understanding Sleep Science",
            help="Title of the episode"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate Button
        if st.button("🎨 Generate CTA Image", type="primary", use_container_width=True):
            with st.spinner("✨ Creating your CTA image..."):
                # Create the CTA image
                cta_image = create_cta_podcast_image(
                    bg_color=bg_color,
                    bg_image=bg_image,
                    cta_label=cta_label,
                    cta_box_color=cta_box_color,
                    guest_name=guest_name,
                    episode_title=episode_title
                )
                
                st.session_state.tab2_cta_image = cta_image
                st.success("✅ CTA image generated successfully!")
    
    with col_right:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;'>
                <h3 style='margin-top: 0;'>👀 Preview</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.tab2_cta_image:
            # Show preview
            st.image(st.session_state.tab2_cta_image, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Download button
            img_bytes = BytesIO()
            st.session_state.tab2_cta_image.save(img_bytes, format='PNG', quality=95)
            img_bytes.seek(0)
            
            st.download_button(
                label="⬇️ Download CTA Image",
                data=img_bytes,
                file_name="podcast_cta.png",
                mime="image/png",
                use_container_width=True,
                type="primary"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.info("""
            **📦 Your CTA includes:**
            - ✅ 1080x1080px Instagram-ready format
            - ✅ Custom background and colors
            - ✅ Professional typography
            - ✅ Rena Malik MD Podcast branding
            
            **💡 Perfect for:**
            - Instagram posts
            - Facebook updates
            - Twitter/X content
            - Newsletter graphics
            """)
        else:
            # Placeholder
            st.markdown("""
                <div style='background: #f7fafc; border: 2px dashed #cbd5e0; border-radius: 16px; 
                            padding: 4rem 2rem; text-align: center; min-height: 500px; 
                            display: flex; align-items: center; justify-content: center;'>
                    <div>
                        <h3 style='color: #718096; margin: 0;'>👈 Customize your CTA on the left</h3>
                        <p style='color: #a0aec0; margin-top: 0.5rem;'>Your preview will appear here</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: CREATE CAROUSEL/FEED POST
# ============================================================================

with tab3:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎨 Multi-Platform Post Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>Upload once, post everywhere. Reach your audience across all platforms</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display configured account IDs in a nice info box
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 1.5rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>📋 Configured Account IDs</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**📷 Instagram**")
        st.text_input("IG ID", value=INSTAGRAM_ACCOUNT_ID, disabled=True, label_visibility="collapsed", key="tab3_ig_display")
    with col2:
        st.markdown("**💼 LinkedIn**")
        st.text_input("LI ID", value=LINKEDIN_ACCOUNT_ID, disabled=True, label_visibility="collapsed", key="tab3_li_display")
    with col3:
        st.markdown("**👥 Facebook**")
        st.text_input("FB ID", value=FACEBOOK_ACCOUNT_ID, disabled=True, label_visibility="collapsed", key="tab3_fb_display")
    with col4:
        st.markdown("**🐦 Twitter**")
        st.text_input("TW ID", value=TWITTER_ACCOUNT_ID, disabled=True, label_visibility="collapsed", key="tab3_tw_display")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
        
        # Compact image preview in collapsible grid
        with st.expander(f"👁️ Preview Uploaded Images ({len(carousel_images)} images)", expanded=False):
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
        # Initialize if needed
        if 'master_content' not in st.session_state:
            st.session_state.master_content = ""
        if 'master_content_key' not in st.session_state:
            st.session_state.master_content_key = 0
        
        # The text_area value should always come from session_state
        # Use a dynamic key that changes when webhook updates
        master_content = st.text_area(
            "✍️ Post Content",
            value=st.session_state.master_content,
            height=150,
            placeholder="Write your post content here... This will be your default content for all platforms.",
            key=f"master_content_input_{st.session_state.master_content_key}"
        )
        
        # Update session state when user types (but not during webhook updates)
        if 'webhook_updating' not in st.session_state:
            st.session_state.webhook_updating = False
        
        if not st.session_state.webhook_updating and master_content != st.session_state.master_content:
            st.session_state.master_content = master_content
        
        # Transcript upload in collapsible section
        with st.expander("📄 Upload Transcript (Optional)"):
            transcript_file_tab3 = st.file_uploader(
                "Drop your transcript file here",
                accept_multiple_files=False,
                type=['txt'],
                key="transcript_tab3",
                help="Upload a .txt transcript file to help generate captions",
                label_visibility="collapsed"
            )
            
            if transcript_file_tab3:
                st.success(f"✅ {transcript_file_tab3.name}")
                transcript_content = transcript_file_tab3.read().decode('utf-8')
                st.text_area("Preview", value=transcript_content[:300] + "..." if len(transcript_content) > 300 else transcript_content, height=100, disabled=True, label_visibility="collapsed")
        
        # Generate Caption button with webhook functionality
        if st.button("✨ Generate Caption", key="generate_caption_tab3", help="Generate caption from images and transcript"):
            if not carousel_images:
                st.warning("⚠️ Please upload images first!")
            else:
                with st.spinner("🔄 Sending data to generate caption..."):
                    try:
                        # First, upload images to GetLate to get public URLs
                        image_urls = []
                        with st.spinner("📤 Uploading images to get public URLs..."):
                            for img in carousel_images:
                                url = upload_image_to_getlate(img, FIXED_API_KEY)
                                if url:
                                    image_urls.append(url)
                        
                        if not image_urls:
                            st.error("❌ Failed to upload images. Please try again.")
                        else:
                            # Prepare data for webhook
                            data = {
                                'image_urls': ','.join(image_urls)  # Send as comma-separated string
                            }
                            
                            # Add transcript as plain text if available
                            if transcript_file_tab3:
                                transcript_file_tab3.seek(0)
                                transcript_text = transcript_file_tab3.read().decode('utf-8')
                                data['transcript'] = transcript_text
                            
                            # Send to webhook as JSON
                            webhook_url = "https://hook.us2.make.com/mz87lk80py2p2dr5dtn924mdjuox2bg7"
                            response = requests.post(webhook_url, json=data, timeout=30)
                            
                            if response.status_code == 200:
                                try:
                                    # Try to parse JSON response
                                    result = response.json()
                                    
                                    # Check if response has caption field
                                    if isinstance(result, dict) and 'caption' in result:
                                        st.session_state.webhook_updating = True
                                        st.session_state.master_content = result['caption']
                                        st.session_state.master_content_key += 1  # Force widget recreation
                                        st.session_state.webhook_updating = False
                                        st.success("✅ Caption generated successfully!")
                                        st.rerun()
                                    else:
                                        # If response is just text, use it directly
                                        response_text = response.text.strip()
                                        if response_text:
                                            st.session_state.webhook_updating = True
                                            st.session_state.master_content = response_text
                                            st.session_state.master_content_key += 1  # Force widget recreation
                                            st.session_state.webhook_updating = False
                                            st.success("✅ Caption generated successfully!")
                                            st.rerun()
                                        else:
                                            st.info("📬 Request sent! Waiting for caption...")
                                except ValueError:
                                    # If not JSON, treat as plain text
                                    response_text = response.text.strip()
                                    if response_text:
                                        st.session_state.webhook_updating = True
                                        st.session_state.master_content = response_text
                                        st.session_state.master_content_key += 1  # Force widget recreation
                                        st.session_state.webhook_updating = False
                                        st.success("✅ Caption generated successfully!")
                                        st.rerun()
                                    else:
                                        st.info("📬 Request sent! Waiting for caption...")
                            else:
                                st.error(f"❌ Failed to send request: {response.status_code}")
                                st.error(f"Response: {response.text}")
                    
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("**📅 Master Schedule (PDT)**")
        
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Platform selection with modern cards - MOVED HERE BEFORE THE BUTTON
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
    
    # Post to All Platforms Section - NOW AFTER THE CHECKBOXES
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
            # Build list of platforms to post to
            platforms_to_post = []
            
            if enable_instagram:
                # Upload images first
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images for Instagram..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, FIXED_API_KEY)
                            if url:
                                media_items.append({"url": url})
                
                platforms_to_post.append({
                    "platform": "Instagram",
                    "accountId": INSTAGRAM_ACCOUNT_ID,
                    "content": st.session_state.get('ig_content_value', st.session_state.master_content),
                    "schedule": st.session_state.get('ig_schedule', st.session_state.master_schedule),
                    "mediaItems": media_items
                })
            
            if enable_linkedin:
                # Upload images first
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images for LinkedIn..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, FIXED_API_KEY)
                            if url:
                                media_items.append({"url": url})
                
                platforms_to_post.append({
                    "platform": "LinkedIn",
                    "accountId": LINKEDIN_ACCOUNT_ID,
                    "content": st.session_state.get('li_content_value', st.session_state.master_content),
                    "schedule": st.session_state.get('li_schedule', st.session_state.master_schedule),
                    "mediaItems": media_items
                })
            
            if enable_facebook:
                # Upload images first
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images for Facebook..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, FIXED_API_KEY)
                            if url:
                                media_items.append({"url": url})
                
                platforms_to_post.append({
                    "platform": "Facebook",
                    "accountId": FACEBOOK_ACCOUNT_ID,
                    "content": st.session_state.get('fb_content_value', st.session_state.master_content),
                    "schedule": st.session_state.get('fb_schedule', st.session_state.master_schedule),
                    "mediaItems": media_items
                })
            
            if enable_twitter:
                # Upload images first
                media_items = []
                if carousel_images:
                    with st.spinner("📤 Uploading images for Twitter..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, FIXED_API_KEY)
                            if url:
                                media_items.append({"url": url})
                
                platforms_to_post.append({
                    "platform": "Twitter",
                    "accountId": TWITTER_ACCOUNT_ID,
                    "content": st.session_state.get('tw_content_value', st.session_state.master_content),
                    "schedule": st.session_state.get('tw_schedule', st.session_state.master_schedule),
                    "mediaItems": media_items
                })
            
            if not platforms_to_post:
                st.error("❌ No platforms configured! Please enable platforms above.")
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
                        
                        response = send_post_to_api(FIXED_API_KEY, payload)
                        
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
    
    # Platform-specific configurations
    platforms_config = []
    
    # Instagram Configuration
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
                st.info(f"Using Account ID: {INSTAGRAM_ACCOUNT_ID}")
                
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
                    st.session_state.ig_schedule = ig_datetime_pdt.isoformat()
                else:
                    st.session_state.ig_schedule = st.session_state.master_schedule
    
    # LinkedIn Configuration
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
                st.info(f"Using Account ID: {LINKEDIN_ACCOUNT_ID}")
                
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
                    st.session_state.li_schedule = li_datetime_pdt.isoformat()
                else:
                    st.session_state.li_schedule = st.session_state.master_schedule
    
    # Facebook Configuration
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
                st.info(f"Using Account ID: {FACEBOOK_ACCOUNT_ID}")
                
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
                    st.session_state.fb_schedule = fb_datetime_pdt.isoformat()
                else:
                    st.session_state.fb_schedule = st.session_state.master_schedule
    
    # Twitter Configuration
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
                st.info(f"Using Account ID: {TWITTER_ACCOUNT_ID}")
                
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
                    st.session_state.tw_schedule = tw_datetime_pdt.isoformat()
                else:
                    st.session_state.tw_schedule = st.session_state.master_schedule
# ============================================================================
# TAB 4: CREATE SHORT FORM VIDEO POST
# ============================================================================

with tab4:
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎬 Short Form Video Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>TikTok, Reels, YouTube Shorts & More - Upload once, post everywhere!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Video upload section with modern card
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>📤 Upload Your Video</h3>
        </div>
    """, unsafe_allow_html=True)
    
    video_file = st.file_uploader(
        "🎥 Drop your video here or click to browse",
        accept_multiple_files=False,
        type=['mp4', 'mov', 'avi', 'mkv'],
        key="video_file",
        help="Upload your short form video (TikTok, Reels, Shorts, etc.)"
    )
    
    # Thumbnail upload
    thumbnail_file = st.file_uploader(
        "🖼️ Upload Thumbnail (Optional for YouTube)",
        accept_multiple_files=False,
        type=['png', 'jpg', 'jpeg'],
        key="thumbnail_file",
        help="Optional: Upload a custom thumbnail for YouTube"
    )
    
    if video_file:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ Video uploaded: {video_file.name}")
        with col2:
            file_size = len(video_file.getvalue()) / (1024 * 1024)  # Convert to MB
            st.metric("📊 Size", f"{file_size:.1f} MB")
    
    if thumbnail_file:
        st.success(f"✅ Thumbnail uploaded: {thumbnail_file.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Master content editor with modern styling
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0; border: 2px solid #667eea;'>
            <h3 style='margin-top: 0; color: #667eea;'>📝 Master Content Editor</h3>
            <p style='color: #4a5568; margin: 0.5rem 0 0 0; font-size: 0.95rem;'>
                ✍️ Create your content once, then customize for each platform below
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize session state for video master content
        if 'video_master_content' not in st.session_state:
            st.session_state.video_master_content = ""
        if 'video_master_content_key' not in st.session_state:
            st.session_state.video_master_content_key = 0
        
        # The text_area value should always come from session_state
        # Use a dynamic key that changes when webhook updates
        video_master_content = st.text_area(
            "✍️ Video Caption/Description",
            value=st.session_state.video_master_content,
            height=150,
            placeholder="Write your video caption/description here... This will be your default content for all platforms.",
            key=f"video_master_content_input_{st.session_state.video_master_content_key}"
        )
        
        # Update session state when user types (but not during webhook updates)
        if 'webhook_updating' not in st.session_state:
            st.session_state.webhook_updating = False
        
        if not st.session_state.webhook_updating and video_master_content != st.session_state.video_master_content:
            st.session_state.video_master_content = video_master_content
        
        # Master tags/hashtags
        video_master_tags = st.text_input(
            "#️⃣ Tags/Hashtags (comma-separated)",
            placeholder="shorts, viral, trending, fun",
            key="video_master_tags"
        )
        
        # Transcript upload in collapsible section
        with st.expander("📄 Upload Transcript (Optional)"):
            transcript_file_tab4 = st.file_uploader(
                "Drop your transcript file here",
                accept_multiple_files=False,
                type=['txt'],
                key="transcript_tab4",
                help="Upload a .txt transcript file to help generate captions",
                label_visibility="collapsed"
            )
            
            if transcript_file_tab4:
                st.success(f"✅ {transcript_file_tab4.name}")
                transcript_content = transcript_file_tab4.read().decode('utf-8')
                st.text_area("Preview", value=transcript_content[:300] + "..." if len(transcript_content) > 300 else transcript_content, height=100, disabled=True, label_visibility="collapsed")
        
        # Generate Caption and Tags buttons with webhook functionality
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✨ Generate Caption", key="generate_caption_tab4", help="Generate caption from transcript"):
                if not transcript_file_tab4:
                    st.warning("⚠️ Please upload a transcript first!")
                else:
                    with st.spinner("🔄 Sending transcript to generate caption..."):
                        try:
                            # Prepare data for webhook
                            data = {}
                            
                            # Add transcript as plain text (required)
                            transcript_file_tab4.seek(0)
                            transcript_text = transcript_file_tab4.read().decode('utf-8')
                            data['transcript'] = transcript_text
                            
                            # Send to webhook as JSON
                            webhook_url = "https://hook.us2.make.com/rloo0d6hstplx6vbr027wrj3cuid9hfb"
                            response = requests.post(webhook_url, json=data, timeout=30)
                            
                            if response.status_code == 200:
                                try:
                                    # Try to parse JSON response
                                    result = response.json()
                                    
                                    # Check if response has caption field
                                    if isinstance(result, dict) and 'caption' in result:
                                        st.session_state.webhook_updating = True
                                        st.session_state.video_master_content = result['caption']
                                        st.session_state.video_master_content_key += 1  # Force widget recreation
                                        st.session_state.webhook_updating = False
                                        st.success("✅ Caption generated successfully!")
                                        st.rerun()
                                    else:
                                        # If response is just text, use it directly
                                        response_text = response.text.strip()
                                        if response_text:
                                            st.session_state.webhook_updating = True
                                            st.session_state.video_master_content = response_text
                                            st.session_state.video_master_content_key += 1  # Force widget recreation
                                            st.session_state.webhook_updating = False
                                            st.success("✅ Caption generated successfully!")
                                            st.rerun()
                                        else:
                                            st.info("📬 Request sent! Waiting for caption...")
                                except ValueError:
                                    # If not JSON, treat as plain text
                                    response_text = response.text.strip()
                                    if response_text:
                                        st.session_state.webhook_updating = True
                                        st.session_state.video_master_content = response_text
                                        st.session_state.video_master_content_key += 1  # Force widget recreation
                                        st.session_state.webhook_updating = False
                                        st.success("✅ Caption generated successfully!")
                                        st.rerun()
                                    else:
                                        st.info("📬 Request sent! Waiting for caption...")
                            else:
                                st.error(f"❌ Failed to send request: {response.status_code}")
                                st.error(f"Response: {response.text}")
                        
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timed out. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with col_btn2:
            if st.button("🏷️ Generate Tags", key="generate_tags_tab4", help="Generate tags from transcript"):
                if not transcript_file_tab4:
                    st.warning("⚠️ Please upload a transcript first!")
                else:
                    with st.spinner("🔄 Sending transcript to generate tags..."):
                        try:
                            # Prepare data for webhook
                            data = {}
                            
                            # Add transcript as plain text (required)
                            transcript_file_tab4.seek(0)
                            transcript_text = transcript_file_tab4.read().decode('utf-8')
                            data['transcript'] = transcript_text
                            
                            # Add request type indicator
                            data['request_type'] = 'tags'
                            
                            # Send to webhook as JSON
                            webhook_url = "https://hook.us2.make.com/rloo0d6hstplx6vbr027wrj3cuid9hfb"
                            response = requests.post(webhook_url, json=data, timeout=30)
                            
                            if response.status_code == 200:
                                st.success("✅ Tags generation request sent successfully!")
                                st.info("📬 Tags will be available shortly. Check your Make.com scenario output.")
                            else:
                                st.error(f"❌ Failed to send request: {response.status_code}")
                                st.error(f"Response: {response.text}")
                        
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timed out. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("**📅 Master Schedule (PDT)**")
        
        default_date = datetime.now() + timedelta(hours=1)
        
        video_master_date = st.date_input(
            "📆 Date", 
            value=default_date,
            key="video_master_date_input"
        )
        video_master_time = st.time_input(
            "🕐 Time", 
            value=default_date.time(),
            key="video_master_time_input"
        )
        
        # Combine date and time
        video_master_datetime = datetime.combine(video_master_date, video_master_time)
        pdt = pytz.timezone('America/Los_Angeles')
        video_master_datetime_pdt = pdt.localize(video_master_datetime)
        video_master_schedule_iso = video_master_datetime_pdt.isoformat()
        
        if 'video_master_schedule' not in st.session_state:
            st.session_state.video_master_schedule = video_master_schedule_iso
        else:
            st.session_state.video_master_schedule = video_master_schedule_iso
    
    # Post to All Platforms Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2.5rem; border-radius: 16px; text-align: center; margin: 1.5rem 0;
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);'>
            <h3 style='margin: 0 0 0.5rem 0; color: #ffffff; font-size: 1.5rem; font-weight: 700;'>
                🚀 Post Video to All Platforms
            </h3>
            <p style='margin: 0; font-size: 1rem; color: #ffffff; opacity: 1;'>
                Upload your video and post to all selected platforms at once
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎬 Post to All Selected Platforms", use_container_width=True, type="primary", key="video_push_to_all_btn"):
            if not video_file:
                st.error("❌ Please upload a video first!")
            else:
                # Upload video first
                with st.spinner("📤 Uploading video to GetLate..."):
                    video_file.seek(0)
                    files = {'files': (video_file.name, video_file, 'video/mp4')}
                    headers = {"Authorization": f"Bearer {FIXED_API_KEY}"}
                    
                    try:
                        response = requests.post(
                            "https://getlate.dev/api/v1/media",
                            headers=headers,
                            files=files
                        )
                        
                        if response.status_code in [200, 201]:
                            result = response.json()
                            video_url = result['files'][0]['url']
                            
                            # Upload thumbnail if provided
                            thumbnail_url = None
                            if thumbnail_file:
                                thumbnail_url = upload_image_to_getlate(thumbnail_file, FIXED_API_KEY)
                            
                            # Build list of platforms to post to
                            platforms_to_post = []
                            
                            if video_enable_youtube and st.session_state.get('yt_account_id'):
                                platforms_to_post.append({
                                    "platform": "YouTube",
                                    "accountId": st.session_state.yt_account_id,
                                    "content": st.session_state.get('yt_content_value', st.session_state.video_master_content),
                                    "schedule": st.session_state.get('yt_schedule', st.session_state.video_master_schedule),
                                    "videoUrl": video_url,
                                    "thumbnailUrl": thumbnail_url,
                                    "platformSpecificData": {
                                        "tags": st.session_state.get('yt_tags', '').split(',') if st.session_state.get('yt_tags') else [],
                                        "videoTitle": st.session_state.get('yt_title', ''),
                                        "videoDescription": st.session_state.get('yt_description', ''),
                                        "videoCategory": st.session_state.get('yt_category', '22'),
                                        "videoPrivacy": st.session_state.get('yt_privacy', 'public'),
                                        "videoLicense": "youtube",
                                        "videoMadeForKids": st.session_state.get('yt_made_for_kids', False),
                                        "videoEmbeddable": True,
                                        "videoNotifySubscribers": st.session_state.get('yt_notify', True)
                                    }
                                })
                            
                            if video_enable_instagram and st.session_state.get('ig_video_account_id'):
                                content_type = st.session_state.get('ig_content_type', 'reel')
                                platform_data = {
                                    "platform": f"Instagram {content_type.title()}",
                                    "accountId": st.session_state.ig_video_account_id,
                                    "content": st.session_state.get('ig_video_content_value', st.session_state.video_master_content),
                                    "schedule": st.session_state.get('ig_video_schedule', st.session_state.video_master_schedule),
                                    "videoUrl": video_url
                                }
                                
                                if content_type == 'story':
                                    platform_data["platformSpecificData"] = {
                                        "contentType": "story"
                                    }
                                
                                platforms_to_post.append(platform_data)
                            
                            if video_enable_tiktok and st.session_state.get('tt_account_id'):
                                platforms_to_post.append({
                                    "platform": "TikTok",
                                    "accountId": st.session_state.tt_account_id,
                                    "content": st.session_state.get('tt_content_value', st.session_state.video_master_content),
                                    "schedule": st.session_state.get('tt_schedule', st.session_state.video_master_schedule),
                                    "videoUrl": video_url,
                                    "platformSpecificData": {
                                        "tiktokSettings": {
                                            "privacy_level": st.session_state.get('tt_privacy', 'public'),
                                            "allow_comment": st.session_state.get('tt_comments', True),
                                            "allow_duet": st.session_state.get('tt_duet', True),
                                            "allow_stitch": st.session_state.get('tt_stitch', True),
                                            "commercial_content_type": st.session_state.get('tt_commercial', False),
                                            "content_preview_confirmed": True,
                                            "express_consent_given": True,
                                            "video_made_with_ai": st.session_state.get('tt_ai', False)
                                        }
                                    }
                                })
                            
                            if video_enable_facebook and st.session_state.get('fb_video_account_id'):
                                content_type = st.session_state.get('fb_video_content_type', 'video')
                                platform_data = {
                                    "platform": f"Facebook {content_type.title()}",
                                    "accountId": st.session_state.fb_video_account_id,
                                    "content": st.session_state.get('fb_video_content_value', st.session_state.video_master_content),
                                    "schedule": st.session_state.get('fb_video_schedule', st.session_state.video_master_schedule),
                                    "videoUrl": video_url
                                }
                                
                                if content_type == 'story':
                                    platform_data["platformSpecificData"] = {
                                        "contentType": "story"
                                    }
                                elif thumbnail_url:
                                    platform_data["thumbnailUrl"] = thumbnail_url
                                    if st.session_state.get('fb_first_comment'):
                                        platform_data["platformSpecificData"] = {
                                            "firstComment": st.session_state.fb_first_comment
                                        }
                                
                                platforms_to_post.append(platform_data)
                            
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
                                        
                                        # Build payload for this platform
                                        payload = {
                                            "content": platform_data['content'],
                                            "scheduledFor": platform_data['schedule'],
                                            "timezone": "America/Los_Angeles",
                                            "platforms": [{
                                                "accountId": platform_data['accountId'],
                                                "mediaItems": [{
                                                    "url": platform_data['videoUrl']
                                                }]
                                            }]
                                        }
                                        
                                        # Add thumbnail if available
                                        if platform_data.get('thumbnailUrl'):
                                            payload["platforms"][0]["mediaItems"][0]["thumbnailUrl"] = platform_data['thumbnailUrl']
                                        
                                        # Add platform-specific data
                                        if platform_data.get('platformSpecificData'):
                                            payload["platforms"][0]["platformSpecificData"] = platform_data['platformSpecificData']
                                        
                                        response = send_post_to_api(FIXED_API_KEY, payload)
                                        
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
                                        st.success(f"🎉 Successfully posted video to all {success_count} platform(s)!")
                                    else:
                                        st.warning(f"⚠️ Posted to {success_count} platform(s), {error_count} failed")
                        else:
                            st.error(f"❌ Failed to upload video: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error uploading video: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Platform selection with modern cards
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>🌐 Select Your Platforms</h3>
            <p style='color: #666; margin: 0;'>Choose which platforms to post your video to</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        video_enable_youtube = st.checkbox("▶️ **YouTube Shorts**", value=False, key="enable_yt")
    with col2:
        video_enable_instagram = st.checkbox("📷 **Instagram**", value=False, key="enable_ig_video")
    with col3:
        video_enable_tiktok = st.checkbox("🎵 **TikTok**", value=False, key="enable_tt")
    with col4:
        video_enable_facebook = st.checkbox("👥 **Facebook**", value=False, key="enable_fb_video")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # YouTube Shorts Configuration
    if video_enable_youtube:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #FF0000;'>▶️ YouTube Shorts Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                yt_account_id = st.text_input(
                    "🆔 YouTube Account ID",
                    key="yt_account_id",
                    placeholder="Enter your YouTube account ID"
                )
                
                if yt_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'yt_content_value' not in st.session_state:
                    st.session_state.yt_content_value = ""
                if 'yt_refresh_counter' not in st.session_state:
                    st.session_state.yt_refresh_counter = 0
                
                yt_title = st.text_input(
                    "📝 Video Title",
                    value="",
                    key="yt_title",
                    placeholder="My Awesome YouTube Short"
                )
                
                yt_description = st.text_area(
                    "💬 Video Description",
                    value=st.session_state.yt_content_value,
                    height=100,
                    key=f"yt_content_area_{st.session_state.yt_refresh_counter}",
                    placeholder="Description for your YouTube Short..."
                )
                if yt_description != st.session_state.yt_content_value:
                    st.session_state.yt_content_value = yt_description
                
                yt_tags = st.text_input(
                    "#️⃣ Tags (comma-separated)",
                    key="yt_tags",
                    placeholder="shorts, fun, video"
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    yt_category = st.selectbox(
                        "📂 Category",
                        options=["22", "1", "2", "10", "15", "17", "19", "20", "23", "24", "25", "26", "27", "28"],
                        key="yt_category",
                        help="22=People & Blogs, 1=Film & Animation, 2=Autos & Vehicles, 10=Music, etc."
                    )
                    
                    yt_privacy = st.selectbox(
                        "🔒 Privacy",
                        options=["public", "unlisted", "private"],
                        key="yt_privacy"
                    )
                
                with col_b:
                    yt_made_for_kids = st.checkbox(
                        "👶 Made for Kids",
                        value=False,
                        key="yt_made_for_kids"
                    )
                    
                    yt_notify = st.checkbox(
                        "🔔 Notify Subscribers",
                        value=True,
                        key="yt_notify"
                    )
            
            with col2:
                use_master_yt = st.button("📋 Use Master", key="yt_use_master_btn", use_container_width=True)
                
                if use_master_yt:
                    st.session_state.yt_content_value = st.session_state.video_master_content
                    if 'yt_refresh_counter' not in st.session_state:
                        st.session_state.yt_refresh_counter = 0
                    st.session_state.yt_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_yt = st.checkbox("Use master schedule", value=True, key="yt_master_sched")
                
                if not use_master_schedule_yt:
                    yt_date = st.date_input("Date", value=default_date, key="yt_schedule_date")
                    yt_time = st.time_input("Time (PDT)", value=default_date.time(), key="yt_schedule_time")
                    yt_datetime = datetime.combine(yt_date, yt_time)
                    yt_datetime_pdt = pdt.localize(yt_datetime)
                    st.session_state.yt_schedule = yt_datetime_pdt.isoformat()
                else:
                    st.session_state.yt_schedule = st.session_state.video_master_schedule
    
    # Instagram Configuration (Reel or Story)
    if video_enable_instagram:
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
                ig_video_account_id = st.text_input(
                    "🆔 Instagram Account ID",
                    key="ig_video_account_id",
                    placeholder="Enter your Instagram account ID"
                )
                
                if ig_video_account_id:
                    st.caption("✅ Account ID saved")
                
                # Content type selector
                ig_content_type = st.radio(
                    "📱 Content Type",
                    options=["reel", "story"],
                    key="ig_content_type",
                    horizontal=True
                )
                
                # Initialize content value in session state
                if 'ig_video_content_value' not in st.session_state:
                    st.session_state.ig_video_content_value = ""
                if 'ig_video_refresh_counter' not in st.session_state:
                    st.session_state.ig_video_refresh_counter = 0
                
                ig_video_content = st.text_area(
                    "💬 Caption",
                    value=st.session_state.ig_video_content_value,
                    height=100,
                    key=f"ig_video_content_area_{st.session_state.ig_video_refresh_counter}",
                    placeholder="Your Instagram caption..."
                )
                if ig_video_content != st.session_state.ig_video_content_value:
                    st.session_state.ig_video_content_value = ig_video_content
            
            with col2:
                use_master_ig_video = st.button("📋 Use Master", key="ig_video_use_master_btn", use_container_width=True)
                
                if use_master_ig_video:
                    st.session_state.ig_video_content_value = st.session_state.video_master_content
                    if 'ig_video_refresh_counter' not in st.session_state:
                        st.session_state.ig_video_refresh_counter = 0
                    st.session_state.ig_video_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_ig = st.checkbox("Use master schedule", value=True, key="ig_video_master_sched")
                
                if not use_master_schedule_ig:
                    ig_video_date = st.date_input("Date", value=default_date, key="ig_video_schedule_date")
                    ig_video_time = st.time_input("Time (PDT)", value=default_date.time(), key="ig_video_schedule_time")
                    ig_video_datetime = datetime.combine(ig_video_date, ig_video_time)
                    ig_video_datetime_pdt = pdt.localize(ig_video_datetime)
                    st.session_state.ig_video_schedule = ig_video_datetime_pdt.isoformat()
                else:
                    st.session_state.ig_video_schedule = st.session_state.video_master_schedule
    
    # TikTok Configuration
    if video_enable_tiktok:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #000000 0%, #EE1D52 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #EE1D52;'>🎵 TikTok Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                tt_account_id = st.text_input(
                    "🆔 TikTok Account ID",
                    key="tt_account_id",
                    placeholder="Enter your TikTok account ID"
                )
                
                if tt_account_id:
                    st.caption("✅ Account ID saved")
                
                # Initialize content value in session state
                if 'tt_content_value' not in st.session_state:
                    st.session_state.tt_content_value = ""
                if 'tt_refresh_counter' not in st.session_state:
                    st.session_state.tt_refresh_counter = 0
                
                tt_content = st.text_area(
                    "💬 Caption",
                    value=st.session_state.tt_content_value,
                    height=100,
                    key=f"tt_content_area_{st.session_state.tt_refresh_counter}",
                    placeholder="Your TikTok caption with hashtags..."
                )
                if tt_content != st.session_state.tt_content_value:
                    st.session_state.tt_content_value = tt_content
                
                st.markdown("**⚙️ TikTok Settings**")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    tt_privacy = st.selectbox(
                        "🔒 Privacy",
                        options=["public", "private", "friends"],
                        key="tt_privacy"
                    )
                    
                    tt_comments = st.checkbox(
                        "💬 Allow Comments",
                        value=True,
                        key="tt_comments"
                    )
                
                with col_b:
                    tt_duet = st.checkbox(
                        "🎭 Allow Duet",
                        value=True,
                        key="tt_duet"
                    )
                    
                    tt_stitch = st.checkbox(
                        "✂️ Allow Stitch",
                        value=True,
                        key="tt_stitch"
                    )
                
                with col_c:
                    tt_commercial = st.checkbox(
                        "💼 Commercial Content",
                        value=False,
                        key="tt_commercial"
                    )
                    
                    tt_ai = st.checkbox(
                        "🤖 Made with AI",
                        value=False,
                        key="tt_ai"
                    )
            
            with col2:
                use_master_tt = st.button("📋 Use Master", key="tt_use_master_btn", use_container_width=True)
                
                if use_master_tt:
                    st.session_state.tt_content_value = st.session_state.video_master_content
                    if 'tt_refresh_counter' not in st.session_state:
                        st.session_state.tt_refresh_counter = 0
                    st.session_state.tt_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_tt = st.checkbox("Use master schedule", value=True, key="tt_master_sched")
                
                if not use_master_schedule_tt:
                    tt_date = st.date_input("Date", value=default_date, key="tt_schedule_date")
                    tt_time = st.time_input("Time (PDT)", value=default_date.time(), key="tt_schedule_time")
                    tt_datetime = datetime.combine(tt_date, tt_time)
                    tt_datetime_pdt = pdt.localize(tt_datetime)
                    st.session_state.tt_schedule = tt_datetime_pdt.isoformat()
                else:
                    st.session_state.tt_schedule = st.session_state.video_master_schedule
    
    # Facebook Configuration (Video or Story)
    if video_enable_facebook:
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
                fb_video_account_id = st.text_input(
                    "🆔 Facebook Account ID",
                    key="fb_video_account_id",
                    placeholder="Enter your Facebook account ID"
                )
                
                if fb_video_account_id:
                    st.caption("✅ Account ID saved")
                
                # Content type selector
                fb_video_content_type = st.radio(
                    "📱 Content Type",
                    options=["video", "story"],
                    key="fb_video_content_type",
                    horizontal=True
                )
                
                # Initialize content value in session state
                if 'fb_video_content_value' not in st.session_state:
                    st.session_state.fb_video_content_value = ""
                if 'fb_video_refresh_counter' not in st.session_state:
                    st.session_state.fb_video_refresh_counter = 0
                
                fb_video_content = st.text_area(
                    "💬 Post Content",
                    value=st.session_state.fb_video_content_value,
                    height=100,
                    key=f"fb_video_content_area_{st.session_state.fb_video_refresh_counter}",
                    placeholder="Your Facebook video post content..."
                )
                if fb_video_content != st.session_state.fb_video_content_value:
                    st.session_state.fb_video_content_value = fb_video_content
                
                if fb_video_content_type == "video":
                    fb_first_comment = st.text_input(
                        "💭 First Comment (Optional)",
                        key="fb_first_comment",
                        placeholder="Let me know what you think about this video!"
                    )
            
            with col2:
                use_master_fb_video = st.button("📋 Use Master", key="fb_video_use_master_btn", use_container_width=True)
                
                if use_master_fb_video:
                    st.session_state.fb_video_content_value = st.session_state.video_master_content
                    if 'fb_video_refresh_counter' not in st.session_state:
                        st.session_state.fb_video_refresh_counter = 0
                    st.session_state.fb_video_refresh_counter += 1
                    st.rerun()
                
                st.markdown("**📅 Schedule**")
                use_master_schedule_fb = st.checkbox("Use master schedule", value=True, key="fb_video_master_sched")
                
                if not use_master_schedule_fb:
                    fb_video_date = st.date_input("Date", value=default_date, key="fb_video_schedule_date")
                    fb_video_time = st.time_input("Time (PDT)", value=default_date.time(), key="fb_video_schedule_time")
                    fb_video_datetime = datetime.combine(fb_video_date, fb_video_time)
                    fb_video_datetime_pdt = pdt.localize(fb_video_datetime)
                    st.session_state.fb_video_schedule = fb_video_datetime_pdt.isoformat()
                else:
                    st.session_state.fb_video_schedule = st.session_state.video_master_schedule
    
    # Individual posting section
    if (video_enable_youtube or video_enable_instagram or video_enable_tiktok or video_enable_facebook):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
                <h3 style='margin-top: 0; text-align: center;'>📤 Individual Platform Posting</h3>
                <p style='color: #666; margin: 0; text-align: center;'>Post to platforms individually with their specific settings</p>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        if video_enable_youtube:
            with cols[0]:
                if st.button("▶️ Post to YouTube", use_container_width=True, key="post_youtube_btn"):
                    if not video_file:
                        st.error("❌ Upload a video first!")
                    elif not st.session_state.get('yt_account_id'):
                        st.error("❌ Enter YouTube Account ID!")
                    else:
                        with st.spinner("📤 Posting to YouTube..."):
                            # Upload video
                            video_file.seek(0)
                            files = {'files': (video_file.name, video_file, 'video/mp4')}
                            headers = {"Authorization": f"Bearer {FIXED_API_KEY}"}
                            response = requests.post("https://getlate.dev/api/v1/media", headers=headers, files=files)
                            
                            if response.status_code in [200, 201]:
                                video_url = response.json()['files'][0]['url']
                                thumbnail_url = None
                                if thumbnail_file:
                                    thumbnail_url = upload_image_to_getlate(thumbnail_file, FIXED_API_KEY)
                                
                                payload = {
                                    "content": st.session_state.get('yt_content_value', ''),
                                    "scheduledFor": st.session_state.get('yt_schedule', st.session_state.video_master_schedule),
                                    "timezone": "America/Los_Angeles",
                                    "platforms": [{
                                        "accountId": st.session_state.yt_account_id,
                                        "platformSpecificData": {
                                            "tags": st.session_state.get('yt_tags', '').split(',') if st.session_state.get('yt_tags') else [],
                                            "videoTitle": st.session_state.get('yt_title', ''),
                                            "videoDescription": st.session_state.get('yt_content_value', ''),
                                            "videoCategory": st.session_state.get('yt_category', '22'),
                                            "videoPrivacy": st.session_state.get('yt_privacy', 'public'),
                                            "videoLicense": "youtube",
                                            "videoMadeForKids": st.session_state.get('yt_made_for_kids', False),
                                            "videoEmbeddable": True,
                                            "videoNotifySubscribers": st.session_state.get('yt_notify', True)
                                        },
                                        "mediaItems": [{"url": video_url, "thumbnailUrl": thumbnail_url}] if thumbnail_url else [{"url": video_url}]
                                    }]
                                }
                                
                                result = send_post_to_api(FIXED_API_KEY, payload)
                                if result and result.status_code in [200, 201]:
                                    st.success("✅ Posted to YouTube!")
                                else:
                                    st.error(f"❌ Failed: {result.json() if result else 'Connection error'}")
        
        if video_enable_instagram:
            with cols[1]:
                if st.button("📷 Post to Instagram", use_container_width=True, key="post_instagram_btn"):
                    if not video_file:
                        st.error("❌ Upload a video first!")
                    elif not st.session_state.get('ig_video_account_id'):
                        st.error("❌ Enter Instagram Account ID!")
                    else:
                        with st.spinner("📤 Posting to Instagram..."):
                            # Upload video
                            video_file.seek(0)
                            files = {'files': (video_file.name, video_file, 'video/mp4')}
                            headers = {"Authorization": f"Bearer {FIXED_API_KEY}"}
                            response = requests.post("https://getlate.dev/api/v1/media", headers=headers, files=files)
                            
                            if response.status_code in [200, 201]:
                                video_url = response.json()['files'][0]['url']
                                
                                payload = {
                                    "content": st.session_state.get('ig_video_content_value', ''),
                                    "scheduledFor": st.session_state.get('ig_video_schedule', st.session_state.video_master_schedule),
                                    "timezone": "America/Los_Angeles",
                                    "platforms": [{
                                        "accountId": st.session_state.ig_video_account_id,
                                        "mediaItems": [{"url": video_url}]
                                    }]
                                }
                                
                                if st.session_state.get('ig_content_type') == 'story':
                                    payload["platforms"][0]["platformSpecificData"] = {"contentType": "story"}
                                
                                result = send_post_to_api(FIXED_API_KEY, payload)
                                if result and result.status_code in [200, 201]:
                                    st.success("✅ Posted to Instagram!")
                                else:
                                    st.error(f"❌ Failed: {result.json() if result else 'Connection error'}")
        
        if video_enable_tiktok:
            with cols[2]:
                if st.button("🎵 Post to TikTok", use_container_width=True, key="post_tiktok_btn"):
                    if not video_file:
                        st.error("❌ Upload a video first!")
                    elif not st.session_state.get('tt_account_id'):
                        st.error("❌ Enter TikTok Account ID!")
                    else:
                        with st.spinner("📤 Posting to TikTok..."):
                            # Upload video
                            video_file.seek(0)
                            files = {'files': (video_file.name, video_file, 'video/mp4')}
                            headers = {"Authorization": f"Bearer {FIXED_API_KEY}"}
                            response = requests.post("https://getlate.dev/api/v1/media", headers=headers, files=files)
                            
                            if response.status_code in [200, 201]:
                                video_url = response.json()['files'][0]['url']
                                
                                payload = {
                                    "content": st.session_state.get('tt_content_value', ''),
                                    "scheduledFor": st.session_state.get('tt_schedule', st.session_state.video_master_schedule),
                                    "timezone": "America/Los_Angeles",
                                    "platforms": [{
                                        "accountId": st.session_state.tt_account_id,
                                        "platformSpecificData": {
                                            "tiktokSettings": {
                                                "privacy_level": st.session_state.get('tt_privacy', 'public'),
                                                "allow_comment": st.session_state.get('tt_comments', True),
                                                "allow_duet": st.session_state.get('tt_duet', True),
                                                "allow_stitch": st.session_state.get('tt_stitch', True),
                                                "commercial_content_type": st.session_state.get('tt_commercial', False),
                                                "content_preview_confirmed": True,
                                                "express_consent_given": True,
                                                "video_made_with_ai": st.session_state.get('tt_ai', False)
                                            }
                                        },
                                        "mediaItems": [{"url": video_url}]
                                    }]
                                }
                                
                                result = send_post_to_api(FIXED_API_KEY, payload)
                                if result and result.status_code in [200, 201]:
                                    st.success("✅ Posted to TikTok!")
                                else:
                                    st.error(f"❌ Failed: {result.json() if result else 'Connection error'}")
        
        if video_enable_facebook:
            with cols[3]:
                if st.button("👥 Post to Facebook", use_container_width=True, key="post_facebook_btn"):
                    if not video_file:
                        st.error("❌ Upload a video first!")
                    elif not st.session_state.get('fb_video_account_id'):
                        st.error("❌ Enter Facebook Account ID!")
                    else:
                        with st.spinner("📤 Posting to Facebook..."):
                            # Upload video
                            video_file.seek(0)
                            files = {'files': (video_file.name, video_file, 'video/mp4')}
                            headers = {"Authorization": f"Bearer {FIXED_API_KEY}"}
                            response = requests.post("https://getlate.dev/api/v1/media", headers=headers, files=files)
                            
                            if response.status_code in [200, 201]:
                                video_url = response.json()['files'][0]['url']
                                thumbnail_url = None
                                if thumbnail_file:
                                    thumbnail_url = upload_image_to_getlate(thumbnail_file, FIXED_API_KEY)
                                
                                payload = {
                                    "content": st.session_state.get('fb_video_content_value', ''),
                                    "scheduledFor": st.session_state.get('fb_video_schedule', st.session_state.video_master_schedule),
                                    "timezone": "America/Los_Angeles",
                                    "platforms": [{
                                        "accountId": st.session_state.fb_video_account_id,
                                        "mediaItems": [{"url": video_url}]
                                    }]
                                }
                                
                                if st.session_state.get('fb_video_content_type') == 'story':
                                    payload["platforms"][0]["platformSpecificData"] = {"contentType": "story"}
                                elif thumbnail_url:
                                    payload["platforms"][0]["mediaItems"][0]["thumbnailUrl"] = thumbnail_url
                                    if st.session_state.get('fb_first_comment'):
                                        payload["platforms"][0]["platformSpecificData"] = {
                                            "firstComment": st.session_state.fb_first_comment
                                        }
                                
                                result = send_post_to_api(FIXED_API_KEY, payload)
                                if result and result.status_code in [200, 201]:
                                    st.success("✅ Posted to Facebook!")
                                else:
                                    st.error(f"❌ Failed: {result.json() if result else 'Connection error'}")
    
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
                        padding: 3rem; border-radius: 16px; text-align: center; margin: 3rem 0;'>
                <h3 style='margin: 0; color: #0c5460;'>👆 Select at least one platform to get started</h3>
                <p style='color: #0c5460; margin: 0.5rem 0 0 0;'>Check the boxes above to enable platforms</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# END OF APPLICATION
# ============================================================================

















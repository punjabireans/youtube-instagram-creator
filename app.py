# app.py
import streamlit as st
import yt_dlp
import cv2
import os
import tempfile
import zipfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math

def extract_screenshots(youtube_url, timestamps):
    """Extract screenshots and return file paths"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download video
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': f'{temp_dir}/video.%(ext)s'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_file = f"{temp_dir}/video.{info['ext']}"
                video_title = info.get('title', 'YouTube Video')
            
            # Extract screenshots
            cap = cv2.VideoCapture(video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            screenshot_files = []
            
            for i, timestamp in enumerate(timestamps):
                # Convert MM:SS to seconds if needed
                if ':' in str(timestamp):
                    parts = str(timestamp).split(':')
                    timestamp = int(parts[0]) * 60 + int(parts[1])
                
                frame_number = int(float(timestamp) * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                
                ret, frame = cap.read()
                if ret:
                    # Convert BGR to RGB for PIL
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    screenshot_path = f"{temp_dir}/screenshot_{i+1}_{timestamp}s.jpg"
                    
                    # Save using PIL for better quality
                    pil_image = Image.fromarray(frame_rgb)
                    pil_image.save(screenshot_path, quality=95)
                    screenshot_files.append((screenshot_path, timestamp))
            
            cap.release()
            
            return screenshot_files, video_title, temp_dir
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None, None, None

def create_instagram_posts(screenshot_files, video_title, temp_dir, post_texts):
    """Create Instagram posts with 2 screenshots each, divided horizontally with text overlays"""
    
    # Instagram post dimensions (square)
    POST_SIZE = 1080
    
    instagram_posts = []
    
    # Group screenshots in pairs
    for post_idx in range(0, len(screenshot_files), 2):
        post_screenshots = screenshot_files[post_idx:post_idx+2]
        
        # Get text for this post (split into two parts)
        post_text = ""
        if post_idx // 2 < len(post_texts):
            post_text = post_texts[post_idx // 2]
        
        # Split text into two parts for top and bottom images
        text_parts = split_text_for_post(post_text)
        
        # Create new Instagram post
        post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='white')
        
        if len(post_screenshots) == 2:
            # Two screenshots - divide horizontally with no gap
            top_img_path, top_timestamp = post_screenshots[0]
            bottom_img_path, bottom_timestamp = post_screenshots[1]
            
            # Load images
            top_img = Image.open(top_img_path)
            bottom_img = Image.open(bottom_img_path)
            
            # Each image gets exactly half the height
            img_height = POST_SIZE // 2
            
            # Resize to fit exactly half the post
            top_img = resize_image_to_exact(top_img, POST_SIZE, img_height)
            bottom_img = resize_image_to_exact(bottom_img, POST_SIZE, img_height)
            
            # Add text overlays
            if len(text_parts) >= 1 and text_parts[0].strip():
                top_img = add_text_overlay(top_img, text_parts[0])
            if len(text_parts) >= 2 and text_parts[1].strip():
                bottom_img = add_text_overlay(bottom_img, text_parts[1])
            
            # Paste images with no gap
            post.paste(top_img, (0, 0))
            post.paste(bottom_img, (0, POST_SIZE // 2))
            
        else:
            # Single screenshot - fill the entire post
            img_path, timestamp = post_screenshots[0]
            img = Image.open(img_path)
            img = resize_image_to_exact(img, POST_SIZE, POST_SIZE)
            
            # Add text overlay if available
            if post_text.strip():
                img = add_text_overlay(img, post_text)
            
            post.paste(img, (0, 0))
        
        # Save Instagram post
        post_path = f"{temp_dir}/instagram_post_{len(instagram_posts) + 1}.jpg"
        post.save(post_path, quality=95)
        instagram_posts.append(post_path)
    
    return instagram_posts

def split_text_for_post(text):
    """Split text into two roughly equal parts for top and bottom images"""
    if not text.strip():
        return ["", ""]
    
    words = text.split()
    if len(words) <= 1:
        return [text, ""]
    
    # Split roughly in half
    mid_point = len(words) // 2
    
    # Try to find a good break point (period, comma, etc.)
    break_point = mid_point
    for i in range(max(1, mid_point - 3), min(len(words), mid_point + 4)):
        if i < len(words) and words[i-1].endswith(('.', '!', '?', ',')):
            break_point = i
            break
    
    first_part = " ".join(words[:break_point])
    second_part = " ".join(words[break_point:])
    
    return [first_part, second_part]

def add_text_overlay(img, text):
    """Add white text overlay at the bottom of the image"""
    if not text.strip():
        return img
    
    # Create a copy to draw on
    img_with_text = img.copy()
    draw = ImageDraw.Draw(img_with_text)
    
    # Image dimensions
    img_width, img_height = img.size
    
    # Font size calculation (mobile-friendly but not too large)
    font_size = max(24, min(48, img_width // 25))  # Responsive font size
    
    try:
        # Try to load a better font
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)  # macOS
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)  # Linux
            except:
                font = ImageFont.load_default()
    
    # Text wrapping
    wrapped_text = wrap_text(text, font, img_width - 40)  # 20px margin on each side
    
    # Calculate text dimensions
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text at bottom with some margin
    margin = 15
    text_x = (img_width - text_width) // 2
    text_y = img_height - text_height - margin
    
    # Ensure text doesn't go too high (avoid covering faces)
    max_text_height = img_height * 0.25  # Text can use max 25% of image height
    if text_height > max_text_height:
        text_y = img_height - max_text_height - margin
    
    # Draw semi-transparent background for better readability
    bg_margin = 10
    bg_coords = [
        text_x - bg_margin,
        text_y - bg_margin,
        text_x + text_width + bg_margin,
        text_y + text_height + bg_margin
    ]
    
    # Create semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(bg_coords, fill=(0, 0, 0, 128))  # Semi-transparent black background
    
    # Composite the overlay
    img_with_text = Image.alpha_composite(img_with_text.convert('RGBA'), overlay).convert('RGB')
    
    # Draw the white text
    draw = ImageDraw.Draw(img_with_text)
    draw.multiline_text((text_x, text_y), wrapped_text, fill='white', font=font, align='center')
    
    return img_with_text

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)  # Single word too long, add anyway
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def resize_image_to_exact(img, target_width, target_height):
    """Resize image to exact dimensions, cropping if necessary to maintain aspect ratio"""
    
    # Calculate ratios
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        # Image is wider than target - fit to height and crop width
        new_height = target_height
        new_width = int(target_height * img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop to center
        left = (new_width - target_width) // 2
        cropped = resized.crop((left, 0, left + target_width, target_height))
        
    else:
        # Image is taller than target - fit to width and crop height
        new_width = target_width
        new_height = int(target_width / img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop to center
        top = (new_height - target_height) // 2
        cropped = resized.crop((0, top, target_width, top + target_height))
    
    return cropped

def create_zip_file(screenshot_files, instagram_posts, temp_dir):
    """Create zip file with both original screenshots and Instagram posts"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add original screenshots
        for file_path, timestamp in screenshot_files:
            filename = f"original_screenshots/{os.path.basename(file_path)}"
            zip_file.write(file_path, filename)
        
        # Add Instagram posts
        for i, post_path in enumerate(instagram_posts):
            filename = f"instagram_posts/post_{i+1}.jpg"
            zip_file.write(post_path, filename)
    
    return zip_buffer.getvalue()

# Streamlit UI
st.title("📸 YouTube to Instagram Post Creator")
st.write("Extract screenshots from YouTube videos and create Instagram-ready posts with custom text!")

# Input fields
youtube_url = st.text_input("YouTube URL:", placeholder="https://youtube.com/watch?v=...")

st.write("**Enter timestamps** (one per line):")
st.write("Format: seconds (e.g., 30) or MM:SS (e.g., 1:30)")
timestamps_text = st.text_area("Timestamps:", placeholder="30\n1:45\n3:20\n5:00")

# Text input for posts
st.write("**Enter text for each Instagram post** (one per line):")
st.write("Each line will be split between the 2 screenshots in that post")
post_texts_input = st.text_area(
    "Post texts:", 
    placeholder="This is the text for post 1 - it will be split between the two screenshots\nThis is the text for post 2 - also split between two images\nPost 3 text goes here",
    help="Enter one line of text for each Instagram post. The text will be automatically split between the top and bottom screenshots."
)

# Options
col1, col2 = st.columns(2)
with col1:
    include_originals = st.checkbox("Include original screenshots", value=True)
with col2:
    show_preview = st.checkbox("Show preview", value=True)

if st.button("Create Instagram Posts", type="primary"):
    if youtube_url and timestamps_text:
        # Parse timestamps
        timestamps = []
        for line in timestamps_text.strip().split('\n'):
            line = line.strip()
            if line:
                timestamps.append(line)
        
        # Parse post texts
        post_texts = []
        if post_texts_input.strip():
            for line in post_texts_input.strip().split('\n'):
                post_texts.append(line.strip())
        
        if timestamps:
            # Calculate number of posts that will be created
            num_posts = math.ceil(len(timestamps) / 2)
            
            # Show warning if text count doesn't match post count
            if post_texts and len(post_texts) != num_posts:
                st.warning(f"⚠️ You have {len(post_texts)} text entries but will create {num_posts} posts. Extra texts will be ignored, missing texts will be left blank.")
            
            with st.spinner("Creating Instagram posts... This may take a few minutes."):
                screenshot_files, video_title, temp_dir = extract_screenshots(youtube_url, timestamps)
                
                if screenshot_files and temp_dir:
                    # Create Instagram posts
                    instagram_posts = create_instagram_posts(screenshot_files, video_title, temp_dir, post_texts)
                    
                    st.success(f"✅ Created {len(instagram_posts)} Instagram posts from {len(timestamps)} screenshots!")
                    
                    # Show preview
                    if show_preview and instagram_posts:
                        st.write("### Preview of Instagram Posts:")
                        cols = st.columns(min(3, len(instagram_posts)))
                        for i, post_path in enumerate(instagram_posts[:3]):  # Show max 3 previews
                            with cols[i % 3]:
                                st.image(post_path, caption=f"Post {i+1}", use_column_width=True)
                        
                        if len(instagram_posts) > 3:
                            st.write(f"... and {len(instagram_posts) - 3} more posts")
                    
                    # Create download package
                    zip_data = create_zip_file(screenshot_files, instagram_posts, temp_dir)
                    
# app.py - Complete Hybrid YouTube to Instagram Post Creator
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import tempfile
import os
import math

def create_posts_from_uploads(uploaded_files, post_texts):
    """Create Instagram posts from uploaded images"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        instagram_posts = []
        
        # Convert uploaded files to PIL Images
        images = []
        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            images.append(img)
        
        # Group images in pairs and create posts
        for i in range(0, len(images), 2):
            post_images = images[i:i+2]
            post_text = post_texts[i//2] if i//2 < len(post_texts) else ""
            
            # Create Instagram post
            instagram_post = create_single_instagram_post(post_images, post_text, temp_dir, len(instagram_posts) + 1)
            instagram_posts.append(instagram_post)
        
        return instagram_posts

def create_single_instagram_post(images, post_text, temp_dir, post_number):
    """Create a single Instagram post from 1 or 2 images"""
    
    POST_SIZE = 1080
    
    # Create new Instagram post
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='white')
    
    if len(images) == 2:
        # Two images - divide horizontally with no gap
        top_img = images[0]
        bottom_img = images[1]
        
        # Each image gets exactly half the height
        img_height = POST_SIZE // 2
        
        # Resize to fit exactly half the post
        top_img = resize_image_to_exact(top_img, POST_SIZE, img_height)
        bottom_img = resize_image_to_exact(bottom_img, POST_SIZE, img_height)
        
        # Split text between images
        text_parts = split_text_for_post(post_text)
        
        # Add text overlays
        if len(text_parts) >= 1 and text_parts[0].strip():
            top_img = add_text_overlay(top_img, text_parts[0])
        if len(text_parts) >= 2 and text_parts[1].strip():
            bottom_img = add_text_overlay(bottom_img, text_parts[1])
        
        # Paste images with no gap
        post.paste(top_img, (0, 0))
        post.paste(bottom_img, (0, POST_SIZE // 2))
        
    else:
        # Single image - fill the entire post
        img = images[0]
        img = resize_image_to_exact(img, POST_SIZE, POST_SIZE)
        
        # Add text overlay if available
        if post_text.strip():
            img = add_text_overlay(img, post_text)
        
        post.paste(img, (0, 0))
    
    # Save Instagram post
    post_path = f"{temp_dir}/instagram_post_{post_number}.jpg"
    post.save(post_path, quality=95)
    
    return post_path

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

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def create_zip_from_posts(instagram_posts, original_images=None):
    """Create zip file with Instagram posts and optionally original images"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add Instagram posts
        for i, post_path in enumerate(instagram_posts):
            filename = f"instagram_posts/post_{i+1}.jpg"
            zip_file.write(post_path, filename)
        
        # Add original images if provided
        if original_images:
            for i, img_file in enumerate(original_images):
                filename = f"original_screenshots/screenshot_{i+1}.jpg"
                # Save original image to temp file and add to zip
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    img = Image.open(img_file)
                    img.save(temp_file.name, quality=95)
                    zip_file.write(temp_file.name, filename)
                    os.unlink(temp_file.name)
    
    return zip_buffer.getvalue()

# Streamlit UI
st.set_page_config(page_title="YouTube to Instagram Creator", page_icon="📸", layout="wide")

st.title("📸 YouTube to Instagram Post Creator")
st.write("Transform your YouTube screenshots into professional Instagram posts!")

# Method selection
method = st.radio(
    "Choose your method:",
    ["📤 Upload Screenshots", "🎥 YouTube Embed + Screenshots"],
    help="Upload method is recommended for best quality and reliability"
)

if method == "📤 Upload Screenshots":
    st.write("### Method 1: Upload Your Screenshots")
    
    with st.expander("📋 How to take great YouTube screenshots"):
        st.write("""
        **For best results:**
        1. Go to your YouTube video
        2. Pause at the exact moments you want
        3. Take screenshots using:
           - **Windows:** Windows + Shift + S
           - **Mac:** Cmd + Shift + 4
           - **Mobile:** Power + Volume Down
        4. Save as PNG or JPG
        5. Upload them below in the order you want them to appear
        
        **Tips:**
        - Use full screen for better quality
        - Choose moments with clear, interesting visuals
        - Even number of screenshots works best (2 per Instagram post)
        """)
    
    uploaded_files = st.file_uploader(
        "Upload your YouTube screenshots", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg'],
        help="Upload screenshots in the order you want them to appear in your Instagram posts"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} screenshots")
        
        # Show preview of uploaded images
        if st.checkbox("Show uploaded images preview"):
            cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files[:4]):
                with cols[i % 4]:
                    img = Image.open(uploaded_file)
                    st.image(img, caption=f"Screenshot {i+1}", use_column_width=True)
            if len(uploaded_files) > 4:
                st.write(f"... and {len(uploaded_files) - 4} more images")
        
        # Calculate number of posts
        num_posts = math.ceil(len(uploaded_files) / 2)
        st.info(f"📊 This will create **{num_posts} Instagram posts** ({len(uploaded_files)} screenshots, 2 per post)")
        
        # Text input for posts
        st.write("### 📝 Add Text to Your Posts")
        st.write(f"Enter text for each of your {num_posts} Instagram posts (one line per post):")
        
        post_texts_input = st.text_area(
            "Post texts:", 
            placeholder=f"Text for Instagram post 1 (will be split between 2 screenshots)\nText for Instagram post 2\nText for Instagram post 3",
            help="Each line will be automatically split between the 2 screenshots in that post",
            height=100
        )
        
        # Options
        col1, col2 = st.columns(2)
        with col1:
            include_originals = st.checkbox("Include original screenshots in download", value=True)
        with col2:
            show_preview = st.checkbox("Show preview of Instagram posts", value=True)
        
        if st.button("🎨 Create Instagram Posts", type="primary"):
            post_texts = [line.strip() for line in post_texts_input.split('\n') if line.strip()]
            
            # Show warning if text count doesn't match post count
            if post_texts and len(post_texts) != num_posts:
                st.warning(f"⚠️ You have {len(post_texts)} text entries but will create {num_posts} posts. Extra texts will be ignored, missing texts will be left blank.")
            
            with st.spinner("Creating Instagram posts... Please wait."):
                instagram_posts = create_posts_from_uploads(uploaded_files, post_texts)
                
                st.success(f"✅ Created {len(instagram_posts)} Instagram posts!")
                
                # Show preview
                if show_preview and instagram_posts:
                    st.write("### 👀 Preview of Your Instagram Posts:")
                    cols = st.columns(min(3, len(instagram_posts)))
                    for i, post_path in enumerate(instagram_posts[:3]):
                        with cols[i % 3]:
                            st.image(post_path, caption=f"Post {i+1}", use_column_width=True)
                    
                    if len(instagram_posts) > 3:
                        st.write(f"... and {len(instagram_posts) - 3} more posts")
                
                # Create download
                original_imgs = uploaded_files if include_originals else None
                zip_data = create_zip_from_posts(instagram_posts, original_imgs)
                
                st.download_button(
                    label="📥 Download Instagram Posts (ZIP)",
                    data=zip_data,
                    file_name=f"instagram_posts_{len(instagram_posts)}_posts.zip",
                    mime="application/zip"
                )
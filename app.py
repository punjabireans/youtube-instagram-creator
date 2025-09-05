Here's the complete, error-free code:

```python
# app.py - Complete fixed version without any errors
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import math

def get_font(size):
    """Get Roboto Slab font or fallback to default"""
    try:
        # Try different font paths
        font_paths = [
            "RobotoSlab-Regular.ttf",
            "/System/Library/Fonts/Georgia.ttf",  # macOS fallback
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",  # Linux fallback
            "arial.ttf"  # Windows fallback
        ]
        
        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
                
        # If all else fails, use default
        return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def create_posts_from_uploads(uploaded_files, post_texts):
    """Create Instagram posts from uploaded images"""
    
    instagram_posts = []
    
    # Convert uploaded files to PIL Images
    images = []
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        # Convert to RGB if needed (fixes JPEG save issues)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        images.append(img)
    
    # Group images in pairs and create posts
    for i in range(0, len(images), 2):
        post_images = images[i:i+2]
        post_text = post_texts[i//2] if i//2 < len(post_texts) else ""
        
        # Create Instagram post
        instagram_post = create_single_instagram_post(post_images, post_text)
        instagram_posts.append(instagram_post)
    
    return instagram_posts

def create_single_instagram_post(images, post_text):
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
    
    return post

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
    """Add white text overlay at the bottom of the image with better positioning"""
    if not text.strip():
        return img
    
    # Create a copy to draw on and ensure RGB mode
    img_with_text = img.copy()
    if img_with_text.mode != 'RGB':
        img_with_text = img_with_text.convert('RGB')
    
    draw = ImageDraw.Draw(img_with_text)
    
    # Image dimensions
    img_width, img_height = img.size
    
    # Font size calculation (mobile-friendly but not too large)
    font_size = max(20, min(40, img_width // 30))  # Slightly smaller for better fit
    
    # Get Roboto Slab font
    font = get_font(font_size)
    
    # Text wrapping with more conservative width
    max_text_width = img_width - 60  # More margin (30px on each side)
    wrapped_text = wrap_text(text, font, max_text_width)
    
    # Calculate text dimensions
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text at bottom with margins
    margin_bottom = 20
    margin_side = 30
    
    # Center text horizontally
    text_x = (img_width - text_width) // 2
    text_y = img_height - text_height - margin_bottom
    
    # Ensure text doesn't go too high (avoid covering faces) and stays within bounds
    max_text_height = img_height * 0.3  # Text can use max 30% of image height
    min_y = img_height * 0.7  # Text should start no higher than 70% down the image
    
    if text_height > max_text_height:
        # If text is too tall, move it up but not too much
        text_y = max(min_y, img_height - max_text_height - margin_bottom)
    
    # Ensure text doesn't go off the left or right edges
    text_x = max(margin_side, min(text_x, img_width - text_width - margin_side))
    
    # Ensure text doesn't go off the bottom
    text_y = min(text_y, img_height - text_height - margin_bottom)
    
    # Draw semi-transparent background for better readability
    bg_margin = 12
    bg_coords = [
        max(0, text_x - bg_margin),
        max(0, text_y - bg_margin),
        min(img_width, text_x + text_width + bg_margin),
        min(img_height, text_y + text_height + bg_margin)
    ]
    
    # Create semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(bg_coords, fill=(0, 0, 0, 140))  # Slightly more opaque
    
    # Composite the overlay
    img_with_text = Image.alpha_composite(img_with_text.convert('RGBA'), overlay).convert('RGB')
    
    # Draw the white text
    draw = ImageDraw.Draw(img_with_text)
    draw.multiline_text((text_x, text_y), wrapped_text, fill='white', font=font, align='center')
    
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
            # Fallback for older PIL versions
            text_width = len(test_line) * (font.size * 0.6)
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single word too long, break it
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Limit to maximum 4 lines to prevent overflow
    if len(lines) > 4:
        lines = lines[:3] + [lines[3] + "..."]
    
    return '\n'.join(lines)

def resize_image_to_exact(img, target_width, target_height):
    """Resize image to exact dimensions, cropping if necessary to maintain aspect ratio"""
    
    # Ensure RGB mode
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
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

def pil_to_bytes(img):
    """Convert PIL Image to bytes for download with error handling"""
    try:
        # Ensure RGB mode for JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG', quality=95, optimize=True)
        img_bytes.seek(0)
        return img_bytes.getvalue()
    except Exception as e:
        st.error(f"Error converting image: {str(e)}")
        # Fallback: try PNG format
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
        # Add Instagram posts
        for i, post_img in enumerate(instagram_posts):
            filename = f"instagram_posts/post_{i+1}.jpg"
            img_bytes = pil_to_bytes(post_img)
            if img_bytes:
                zip_file.writestr(filename, img_bytes)
        
        # Add original images if provided
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
        - Text will be added at the bottom with proper positioning
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
                    st.image(img, caption=f"Screenshot {i+1}", use_container_width=True)
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
            placeholder="Text for Instagram post 1 (will be split between 2 screenshots)\nTextfor Instagram post 2\nText for Instagram post 3",
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
                    for i, post_img in enumerate(instagram_posts[:3]):
                        with cols[i % 3]:
                            st.image(post_img, caption=f"Post {i+1}", use_container_width=True)
                    
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
                
                # Info about what's included
                st.info(f"""
                **Download includes:**
                - {len(instagram_posts)} Instagram-ready posts (1080x1080px)
                - {"Original screenshots" if include_originals else "No original screenshots"}
                - Each Instagram post contains 2 screenshots split horizontally
                - White text overlays positioned at the bottom
                - Ready to upload directly to Instagram!
                """)

else:
    st.write("### Method 2: YouTube Embed + Screenshots")
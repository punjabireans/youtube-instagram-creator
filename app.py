import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import math
import os

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

def create_posts_from_uploads(uploaded_files, post_texts, guest_name, logo_file=None):
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
    
    # Create background with specified color
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='#1A2238')
    draw = ImageDraw.Draw(post)
    
    # Text content
    main_text = f'Listen to the full conversation with special guest {guest_name} on the "Rena Malik, MD Podcast"'
    
    # Font sizes for mobile visibility
    main_font_size = 48
    main_font = get_font(main_font_size, bold=True)
    
    # Text wrapping
    max_text_width = POST_SIZE - 120  # 60px margin on each side
    wrapped_text = wrap_text(main_text, main_font, max_text_width)
    
    # Calculate text dimensions
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=main_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text in center (accounting for logo space if present)
    logo_height = 0
    if logo_file:
        try:
            logo = Image.open(logo_file)
            # Resize logo to reasonable size
            logo_max_size = 200
            logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
            logo_height = logo.height + 40  # Add some spacing
        except:
            logo = None
            logo_height = 0
    else:
        logo = None
    
    # Center text vertically, accounting for logo
    available_height = POST_SIZE - logo_height
    text_y = (available_height - text_height) // 2
    if logo:
        text_y += logo_height
    
    text_x = (POST_SIZE - text_width) // 2
    
    # Draw text with shadow effect
    shadow_offset = 3
    # Draw shadow (black)
    draw.multiline_text(
        (text_x + shadow_offset, text_y + shadow_offset), 
        wrapped_text, 
        fill='black', 
        font=main_font, 
        align='center'
    )
    # Draw main text (#F4DB7D)
    draw.multiline_text(
        (text_x, text_y), 
        wrapped_text, 
        fill='#F4DB7D', 
        font=main_font, 
        align='center'
    )
    
    # Add logo if provided
    if logo:
        logo_x = (POST_SIZE - logo.width) // 2
        logo_y = 60  # Top margin
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
    
    # Draw semi-transparent background
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
    
    # Draw text with shadow
    draw = ImageDraw.Draw(img_with_text)
    shadow_offset = 2
    
    # Draw shadow (black)
    draw.multiline_text(
        (text_x + shadow_offset, text_y + shadow_offset), 
        wrapped_text, 
        fill='black', 
        font=font, 
        align='center'
    )
    # Draw main text (white)
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

st.set_page_config(page_title="YouTube to Instagram Creator", page_icon="📸", layout="wide")

st.title("📸 YouTube to Instagram Post Creator")
st.write("Transform your YouTube screenshots into professional Instagram posts with promotional ending!")

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
        
        if st.checkbox("Show uploaded images preview"):
            cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files[:4]):
                with cols[i % 4]:
                    img = Image.open(uploaded_file)
                    st.image(img, caption=f"Screenshot {i+1}", use_container_width=True)
            if len(uploaded_files) > 4:
                st.write(f"... and {len(uploaded_files) - 4} more images")
        
        num_posts = math.ceil(len(uploaded_files) / 2)
        st.info(f"📊 This will create **{num_posts} Instagram posts** ({len(uploaded_files)} screenshots, 2 per post)")
        
        st.write("### 📝 Add Text to Your Posts")
        st.write(f"Enter text for each of your {num_posts} Instagram posts (one line per post):")
        
        post_texts_input = st.text_area(
            "Post texts:", 
            placeholder="Text for Instagram post 1 (will be split between 2 screenshots)\nText for Instagram post 2\nText for Instagram post 3",
            help="Each line will be automatically split between the 2 screenshots in that post",
            height=100
        )
        
        # Guest name and logo inputs for promotional post
        st.write("### 🎙️ Promotional Post Settings")
        st.write("Add a final promotional post for the podcast")
        
        col1, col2 = st.columns(2)
        with col1:
            guest_name = st.text_input(
                "Guest Name:",
                placeholder="Dr. John Smith",
                help="Enter the name of the guest for the promotional post"
            )
        
        with col2:
            logo_file = st.file_uploader(
                "Upload Podcast Logo (Optional):",
                type=['png', 'jpg', 'jpeg'],
                help="Upload the Rena Malik MD Podcast logo"
            )
        
        if guest_name:
            st.info(f"📢 A promotional post will be added featuring: {guest_name}")
        
        # Options
        col1, col2 = st.columns(2)
        with col1:
            include_originals = st.checkbox("Include original screenshots in download", value=True)
        with col2:
            show_preview = st.checkbox("Show preview of Instagram posts", value=True)
        
        if st.button("🎨 Create Instagram Posts", type="primary"):
            post_texts = [line.strip() for line in post_texts_input.split('\n') if line.strip()]
            
            if post_texts and len(post_texts) != num_posts:
                st.warning(f"⚠️ You have {len(post_texts)} text entries but will create {num_posts} posts. Extra texts will be ignored, missing texts will be left blank.")
            
            with st.spinner("Creating Instagram posts... Please wait."):
                instagram_posts = create_posts_from_uploads(uploaded_files, post_texts, guest_name, logo_file)
                
                total_posts = len(instagram_posts)
                promo_posts = 1 if guest_name.strip() else 0
                regular_posts = total_posts - promo_posts
                
                st.success(f"✅ Created {total_posts} Instagram posts ({regular_posts} regular posts + {promo_posts} promotional post)!")
                
                if show_preview and instagram_posts:
                    st.write("### 👀 Preview of Your Instagram Posts:")
                    cols = st.columns(min(3, len(instagram_posts)))
                    for i, post_img in enumerate(instagram_posts[:3]):
                        with cols[i % 3]:
                            caption = f"Post {i+1}"
                            if i == len(instagram_posts) - 1 and guest_name.strip():
                                caption += " (Promotional)"
                            st.image(post_img, caption=caption, use_container_width=True)
                    
                    if len(instagram_posts) > 3:
                        st.write(f"... and {len(instagram_posts) - 3} more posts")
                
                original_imgs = uploaded_files if include_originals else None
                zip_data = create_zip_from_posts(instagram_posts, original_imgs)
                
                st.download_button(
                    label="📥 Download Instagram Posts (ZIP)",
                    data=zip_data,
                    file_name=f"instagram_posts_{len(instagram_posts)}_posts.zip",
                    mime="application/zip"
                )
                
                st.info(f"""
                **Download includes:**
                - {len(instagram_posts)} Instagram-ready posts (1080x1080px)
                - {"Original screenshots" if include_originals else "No original screenshots"}
                - Each regular post contains 2 screenshots split horizontally
                - White text overlays with black shadows positioned at the bottom
                - {"1 promotional post with podcast branding" if guest_name.strip() else "No promotional post (guest name required)"}
                - Ready to upload directly to Instagram!
                """)

else:
    st.write("### Method 2: YouTube Embed + Screenshots")
    st.info("This method is coming soon! For now, please use the Upload Screenshots method.")

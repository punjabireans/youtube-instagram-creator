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

# ============================================================================
# FONT UTILITIES
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
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1A2238;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        font-size: 16px;
        font-weight: 600;
    }
    .platform-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 Content Posting Automations</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Streamline your content creation and multi-platform posting workflow</p>', unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'master_content' not in st.session_state:
    st.session_state.master_content = ""
if 'master_schedule' not in st.session_state:
    st.session_state.master_schedule = None

# API Key in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "GetLate API Key", 
        type="password", 
        value=st.session_state.api_key,
        help="Enter your GetLate API key for posting"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key saved")
    
    st.divider()
    st.markdown("### 📚 Resources")
    st.markdown("[GetLate Documentation](https://getlate.dev/docs)")
    st.markdown("[API Reference](https://getlate.dev/api)")

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "📸 YouTube to Instagram", 
    "🎨 Create Carousel/Feed Post", 
    "🎬 Create Short Form Video Post"
])

# ============================================================================
# TAB 1: YOUTUBE TO INSTAGRAM
# ============================================================================

with tab1:
    st.header("📸 YouTube to Instagram Post Creator")
    st.markdown("Transform your YouTube screenshots into professional Instagram carousel posts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload Screenshots")
        
        with st.expander("💡 Tips for great screenshots", expanded=False):
            st.markdown("""
            **Best practices:**
            - 🎥 Go fullscreen for better quality
            - ⏸️ Pause at interesting moments
            - 📸 Use 2 screenshots per Instagram post
            - 💾 Save as PNG or JPG
            
            **Keyboard shortcuts:**
            - Windows: `Win + Shift + S`
            - Mac: `Cmd + Shift + 4`
            - Mobile: `Power + Volume Down`
            """)
        
        uploaded_files = st.file_uploader(
            "Drop your screenshots here", 
            accept_multiple_files=True, 
            type=['png', 'jpg', 'jpeg'],
            help="Upload in the order you want them to appear"
        )
    
    with col2:
        if uploaded_files:
            st.metric("Images Uploaded", len(uploaded_files))
            num_posts = math.ceil(len(uploaded_files) / 2)
            st.metric("Posts to Create", num_posts)
            st.info("2 images per post")
    
    if uploaded_files:
        st.divider()
        
        # Image preview in a nice grid
        st.subheader("🖼️ Your Screenshots")
        cols = st.columns(4)
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 4]:
                img = Image.open(uploaded_file)
                st.image(img, caption=f"#{i+1}", use_container_width=True)
        
        st.divider()
        
        # Text input section
        st.subheader("✍️ Add Captions")
        num_posts = math.ceil(len(uploaded_files) / 2)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            post_texts_input = st.text_area(
                f"Enter captions for your {num_posts} posts", 
                placeholder="Caption for post 1 (will split across 2 images)\nCaption for post 2\nCaption for post 3...",
                height=150,
                help="One line per post. Text will be split between the 2 images automatically."
            )
        
        with col2:
            st.markdown("**Options**")
            include_originals = st.checkbox("Include originals in ZIP", value=True)
            guest_name = st.text_input("Guest name (optional)", placeholder="Dr. Jane Smith")
            logo_file = st.file_uploader("Podcast logo", type=['png', 'jpg', 'jpeg'])
        
        # Create button
        if st.button("🎨 Generate Instagram Posts", type="primary", use_container_width=True):
            post_texts = [line.strip() for line in post_texts_input.split('\n') if line.strip()]
            
            with st.spinner("✨ Creating your Instagram posts..."):
                instagram_posts = create_posts_from_uploads(
                    uploaded_files, 
                    post_texts, 
                    guest_name, 
                    logo_file
                )
                
                st.success(f"🎉 Created {len(instagram_posts)} Instagram posts!")
                
                # Show preview in a beautiful grid
                st.subheader("👀 Preview Your Posts")
                cols = st.columns(3)
                for i, post_img in enumerate(instagram_posts):
                    with cols[i % 3]:
                        st.image(post_img, caption=f"Post {i+1}", use_container_width=True)
                
                # Download section
                st.divider()
                original_imgs = uploaded_files if include_originals else None
                zip_data = create_zip_from_posts(instagram_posts, original_imgs)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 Download All Posts (ZIP)",
                        data=zip_data,
                        file_name=f"instagram_posts_{len(instagram_posts)}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                
                st.info(f"""
                **📦 Your download includes:**
                - {len(instagram_posts)} Instagram-ready posts (1080x1080px)
                - {"✅ Original screenshots" if include_originals else ""}
                - Ready to upload to Instagram!
                """)

# ============================================================================
# TAB 2: CREATE CAROUSEL/FEED POST
# ============================================================================

with tab2:
    st.header("🎨 Create Carousel/Feed Post")
    st.markdown("Upload images, add captions, and post to multiple platforms simultaneously")
    
    # Check API key
    if not st.session_state.api_key:
        st.warning("⚠️ Please enter your GetLate API Key in the sidebar to use this feature")
    
    st.divider()
    
    # Image upload section
    st.subheader("📤 Upload Media")
    carousel_images = st.file_uploader(
        "Upload images for your post",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        key="carousel_images"
    )
    
    if carousel_images:
        st.success(f"✅ {len(carousel_images)} image(s) uploaded")
        cols = st.columns(min(5, len(carousel_images)))
        for i, img_file in enumerate(carousel_images[:5]):
            with cols[i]:
                img = Image.open(img_file)
                st.image(img, use_container_width=True)
        if len(carousel_images) > 5:
            st.info(f"... and {len(carousel_images) - 5} more images")
    
    st.divider()
    
    # Master content editor
    st.subheader("📝 Master Content Editor")
    st.markdown("Edit your post content here, then push to specific platforms")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        master_content = st.text_area(
            "Post Content",
            value=st.session_state.master_content,
            height=150,
            placeholder="Write your post content here...",
            key="master_content_input"
        )
        st.session_state.master_content = master_content
    
    with col2:
        st.markdown("**Master Schedule**")
        
        # Date and time picker
        default_date = datetime.now() + timedelta(hours=1)
        master_date = st.date_input("Date", value=default_date)
        master_time = st.time_input("Time (PDT)", value=default_date.time())
        
        # Combine date and time
        master_datetime = datetime.combine(master_date, master_time)
        pdt = pytz.timezone('America/Los_Angeles')
        master_datetime_pdt = pdt.localize(master_datetime)
        master_schedule_iso = master_datetime_pdt.isoformat()
        
        st.session_state.master_schedule = master_schedule_iso
        
        if st.button("📋 Push to All Platforms", use_container_width=True):
            st.session_state.push_to_all = True
            st.success("Content pushed to all platforms!")
    
    st.divider()
    
    # Platform selection
    st.subheader("🌐 Select Platforms")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        enable_instagram = st.checkbox("📷 Instagram", value=False)
    with col2:
        enable_linkedin = st.checkbox("💼 LinkedIn", value=False)
    with col3:
        enable_facebook = st.checkbox("👥 Facebook", value=False)
    with col4:
        enable_twitter = st.checkbox("🐦 Twitter", value=False)
    
    st.divider()
    
    # Platform-specific configurations
    platforms_config = []
    
    # Instagram Configuration
    if enable_instagram:
        with st.expander("📷 Instagram Configuration", expanded=True):
            st.markdown("### Instagram Post Settings")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                ig_account_id = st.text_input(
                    "Account ID",
                    key="ig_account",
                    placeholder="INSTAGRAM_ACCOUNT_ID"
                )
                
                ig_content = st.text_area(
                    "Caption",
                    value=st.session_state.master_content if st.session_state.get('push_to_all') else "",
                    height=100,
                    key="ig_content",
                    placeholder="Your Instagram caption..."
                )
            
            with col2:
                if st.button("📋 Use Master Content", key="ig_use_master"):
                    st.session_state.ig_content = st.session_state.master_content
                    st.rerun()
                
                st.markdown("**Schedule**")
                use_master_schedule = st.checkbox("Use master schedule", value=True, key="ig_master_sched")
                
                if not use_master_schedule:
                    ig_date = st.date_input("Date", value=default_date, key="ig_date")
                    ig_time = st.time_input("Time (PDT)", value=default_date.time(), key="ig_time")
                    ig_datetime = datetime.combine(ig_date, ig_time)
                    ig_datetime_pdt = pdt.localize(ig_datetime)
                    ig_schedule = ig_datetime_pdt.isoformat()
                else:
                    ig_schedule = st.session_state.master_schedule
            
            if ig_account_id:
                # Upload images to GetLate first
                media_items = []
                if carousel_images:
                    with st.spinner("Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Instagram",
                    "accountId": ig_account_id,
                    "content": ig_content,
                    "schedule": ig_schedule,
                    "mediaItems": media_items
                })
    
    # LinkedIn Configuration
    if enable_linkedin:
        with st.expander("💼 LinkedIn Configuration", expanded=True):
            st.markdown("### LinkedIn Post Settings")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                li_account_id = st.text_input(
                    "Account ID",
                    key="li_account",
                    placeholder="LINKEDIN_ACCOUNT_ID"
                )
                
                li_content = st.text_area(
                    "Post Content",
                    value=st.session_state.master_content if st.session_state.get('push_to_all') else "",
                    height=100,
                    key="li_content",
                    placeholder="Your LinkedIn post..."
                )
            
            with col2:
                if st.button("📋 Use Master Content", key="li_use_master"):
                    st.session_state.li_content = st.session_state.master_content
                    st.rerun()
                
                st.markdown("**Schedule**")
                use_master_schedule_li = st.checkbox("Use master schedule", value=True, key="li_master_sched")
                
                if not use_master_schedule_li:
                    li_date = st.date_input("Date", value=default_date, key="li_date")
                    li_time = st.time_input("Time (PDT)", value=default_date.time(), key="li_time")
                    li_datetime = datetime.combine(li_date, li_time)
                    li_datetime_pdt = pdt.localize(li_datetime)
                    li_schedule = li_datetime_pdt.isoformat()
                else:
                    li_schedule = st.session_state.master_schedule
            
            if li_account_id:
                # Upload images to GetLate first
                media_items = []
                if carousel_images:
                    with st.spinner("Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "LinkedIn",
                    "accountId": li_account_id,
                    "content": li_content,
                    "schedule": li_schedule,
                    "mediaItems": media_items
                })
    
    # Facebook Configuration
    if enable_facebook:
        with st.expander("👥 Facebook Configuration", expanded=True):
            st.markdown("### Facebook Post Settings")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fb_account_id = st.text_input(
                    "Account ID",
                    key="fb_account",
                    placeholder="FACEBOOK_ACCOUNT_ID"
                )
                
                fb_content = st.text_area(
                    "Post Content",
                    value=st.session_state.master_content if st.session_state.get('push_to_all') else "",
                    height=100,
                    key="fb_content",
                    placeholder="Your Facebook post..."
                )
            
            with col2:
                if st.button("📋 Use Master Content", key="fb_use_master"):
                    st.session_state.fb_content = st.session_state.master_content
                    st.rerun()
                
                st.markdown("**Schedule**")
                use_master_schedule_fb = st.checkbox("Use master schedule", value=True, key="fb_master_sched")
                
                if not use_master_schedule_fb:
                    fb_date = st.date_input("Date", value=default_date, key="fb_date")
                    fb_time = st.time_input("Time (PDT)", value=default_date.time(), key="fb_time")
                    fb_datetime = datetime.combine(fb_date, fb_time)
                    fb_datetime_pdt = pdt.localize(fb_datetime)
                    fb_schedule = fb_datetime_pdt.isoformat()
                else:
                    fb_schedule = st.session_state.master_schedule
            
            if fb_account_id:
                # Upload images to GetLate first
                media_items = []
                if carousel_images:
                    with st.spinner("Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Facebook",
                    "accountId": fb_account_id,
                    "content": fb_content,
                    "schedule": fb_schedule,
                    "mediaItems": media_items
                })
    
    # Twitter Configuration
    if enable_twitter:
        with st.expander("🐦 Twitter Configuration", expanded=True):
            st.markdown("### Twitter Post Settings")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                tw_account_id = st.text_input(
                    "Account ID",
                    key="tw_account",
                    placeholder="TWITTER_ACCOUNT_ID"
                )
                
                tw_content = st.text_area(
                    "Tweet Content",
                    value=st.session_state.master_content if st.session_state.get('push_to_all') else "",
                    height=100,
                    key="tw_content",
                    placeholder="Your tweet...",
                    max_chars=280
                )
                
                char_count = len(tw_content)
                if char_count > 280:
                    st.error(f"⚠️ Tweet is {char_count - 280} characters over the limit!")
                else:
                    st.info(f"Characters: {char_count}/280")
            
            with col2:
                if st.button("📋 Use Master Content", key="tw_use_master"):
                    st.session_state.tw_content = st.session_state.master_content
                    st.rerun()
                
                st.markdown("**Schedule**")
                use_master_schedule_tw = st.checkbox("Use master schedule", value=True, key="tw_master_sched")
                
                if not use_master_schedule_tw:
                    tw_date = st.date_input("Date", value=default_date, key="tw_date")
                    tw_time = st.time_input("Time (PDT)", value=default_date.time(), key="tw_time")
                    tw_datetime = datetime.combine(tw_date, tw_time)
                    tw_datetime_pdt = pdt.localize(tw_datetime)
                    tw_schedule = tw_datetime_pdt.isoformat()
                else:
                    tw_schedule = st.session_state.master_schedule
            
            if tw_account_id:
                # Upload images to GetLate first
                media_items = []
                if carousel_images:
                    with st.spinner("Uploading images to GetLate..."):
                        for img in carousel_images:
                            url = upload_image_to_getlate(img, st.session_state.api_key)
                            if url:
                                media_items.append({"url": url})
                
                platforms_config.append({
                    "platform": "Twitter",
                    "accountId": tw_account_id,
                    "content": tw_content,
                    "schedule": tw_schedule,
                    "mediaItems": media_items
                })
    
    # Preview and Submit Section
    if platforms_config:
        st.divider()
        st.subheader("👀 Preview Your Posts")
        
        # Show preview for each platform
        for platform_data in platforms_config:
            with st.expander(f"Preview: {platform_data['platform']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Content:**")
                    st.info(platform_data['content'] if platform_data['content'] else "_No content_")
                    
                    if platform_data['mediaItems']:
                        st.markdown(f"**Media:** {len(platform_data['mediaItems'])} image(s)")
                
                with col2:
                    st.markdown(f"**Account ID:**")
                    st.code(platform_data['accountId'])
                    
                    st.markdown(f"**Scheduled for:**")
                    schedule_time = datetime.fromisoformat(platform_data['schedule'])
                    st.write(schedule_time.strftime("%B %d, %Y at %I:%M %p PDT"))
        
        st.divider()
        
        # Final API payload preview
        with st.expander("🔍 View API Payload", expanded=False):
            # Create individual payloads for each platform
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
                
                st.markdown(f"**{platform_data['platform']} Payload:**")
                st.json(payload)
                st.divider()
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Schedule Posts to All Platforms", type="primary", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("❌ Please enter your API key in the sidebar!")
                else:
                    with st.spinner("📤 Scheduling your posts..."):
                        success_count = 0
                        error_count = 0
                        
                        # Send request for each platform
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
                            
                            response = send_post_to_api(st.session_state.api_key, payload)
                            
                            if response and response.status_code in [200, 201]:
                                success_count += 1
                                st.success(f"✅ {platform_data['platform']}: Post scheduled successfully!")
                            else:
                                error_count += 1
                                error_msg = response.json() if response else "Connection error"
                                st.error(f"❌ {platform_data['platform']}: Failed to schedule post")
                                st.error(f"Error: {error_msg}")
                        
                        st.divider()
                        
                        if error_count == 0:
                            st.balloons()
                            st.success(f"🎉 All {success_count} posts scheduled successfully!")
                        else:
                            st.warning(f"⚠️ {success_count} successful, {error_count} failed")
    
    else:
        st.info("👆 Select at least one platform above to get started")

# ============================================================================
# TAB 3: CREATE SHORT FORM VIDEO POST
# ============================================================================

with tab3:
    st.header("🎬 Create Short Form Video Post")
    st.markdown("Post short-form videos to TikTok, Instagram Reels, YouTube Shorts, and more")
    
    st.info("🚧 This feature is coming soon! Stay tuned for updates.")
    
    # Placeholder content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📱 TikTok")
        st.markdown("Upload and schedule TikTok videos")
        st.button("Coming Soon", disabled=True, key="tiktok_btn")
    
    with col2:
        st.markdown("### 🎥 Instagram Reels")
        st.markdown("Create and post Instagram Reels")
        st.button("Coming Soon", disabled=True, key="reels_btn")
    
    with col3:
        st.markdown("### ▶️ YouTube Shorts")
        st.markdown("Upload YouTube Shorts")
        st.button("Coming Soon", disabled=True, key="shorts_btn")
    
    st.divider()
    
    st.markdown("""
    ### 🎯 Planned Features:
    - 📤 Upload video files (MP4, MOV, etc.)
    - ✂️ Video trimming and editing
    - 📝 Add captions and hashtags
    - 🎵 Background music selection
    - 📊 Cross-platform analytics
    - ⏰ Optimal posting time suggestions
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Made with ❤️ for content creators | <a href='https://getlate.dev' target='_blank'>Powered by GetLate</a></p>
</div>
""", unsafe_allow_html=True)

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
        min-width: 21rem !important; 
    }
    
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label { 
        color: white !important; 
    }
    
    section[data-testid="stSidebar"] a {
        color: rgba(255, 255, 255, 0.9) !important;
        text-decoration: none;
    }
    
    section[data-testid="stSidebar"] a:hover {
        color: white !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input, 
    .stTextArea textarea {
        border-radius: 12px; 
        border: 2px solid #e2e8f0; 
        padding: 12px 16px; 
        font-size: 15px; 
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea textarea:focus { 
        border-color: #667eea; 
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); 
    }
    
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
        transition: all 0.3s ease; 
    }
    
    .stButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); 
    }
    
    .stButton > button[kind="primary"] { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white !important; 
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #667eea !important;
        border: 2px solid #667eea;
    }
    
    /* File Uploader */
    .stFileUploader { 
        border-radius: 16px; 
        border: 2px dashed #667eea; 
        padding: 2rem; 
        background: #f7fafc; 
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Messages */
    .stSuccess { 
        background: #d4edda; 
        color: #155724; 
        border-radius: 12px; 
        padding: 16px 20px; 
    }
    
    .stError { 
        background: #f8d7da; 
        color: #721c24; 
        border-radius: 12px; 
        padding: 16px 20px; 
    }
    
    .stInfo { 
        background: #d1ecf1; 
        color: #0c5460; 
        border-radius: 12px; 
        padding: 16px 20px; 
    }
    
    .stWarning { 
        background: #fff3cd; 
        color: #856404; 
        border-radius: 12px; 
        padding: 16px 20px; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 Content Posting Automations</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Streamline your content creation and multi-platform posting workflow</p>', unsafe_allow_html=True)

# Initialize session state
session_defaults = {
    'api_key': '', 'master_content': '', 'master_schedule': None,
    'ig_account_id': '', 'li_account_id': '', 'fb_account_id': '', 'tw_account_id': '',
    'generated_ig_posts': None, 'show_ig_posting': False, 'post_texts_for_ig': []
}

for key, default in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    api_key = st.text_input(
        "🔑 GetLate API Key", 
        type="password", 
        value=st.session_state.api_key,
        help="Enter your GetLate API key for posting",
        placeholder="Enter your API key..."
    )
    
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
    
    # Show saved accounts
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
                for key in ['api_key', 'ig_account_id', 'li_account_id', 'fb_account_id', 'tw_account_id']:
                    st.session_state[key] = ""
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
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📸 YouTube to Instagram</h1>
            <p style='font-size: 1.1rem; color: #666;'>Transform your YouTube screenshots into stunning Instagram carousel posts</p>
        </div>
    """, unsafe_allow_html=True)
    
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
        
        # Image preview
        st.markdown("### 🖼️ Your Screenshots")
        cols = st.columns(4)
        for i, uploaded_file in enumerate(uploaded_files):
            with cols[i % 4]:
                img = Image.open(uploaded_file)
                st.image(img, caption=f"Screenshot {i+1}", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Text input section
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
                <h3 style='margin-top: 0;'>✍️ Add Captions to Your Posts</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        # Create button
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
                    
                    st.session_state.generated_ig_posts = instagram_posts
                    st.session_state.post_texts_for_ig = post_texts
                    
                    st.success(f"🎉 Successfully created {len(instagram_posts)} Instagram posts!")
                    
                    # Show preview
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 👀 Preview Your Amazing Posts")
                    cols = st.columns(3)
                    for i, post_img in enumerate(instagram_posts):
                        with cols[i % 3]:
                            st.image(post_img, caption=f"Post {i+1}", use_container_width=True)
                    
                    # Download section
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
                st.warning("⚠️ Please enter your Instagram Account ID in Tab 3 first")
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
                
                # Post button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Post All to Instagram Now", type="primary", use_container_width=True, key="post_to_ig_btn"):
                        with st.spinner("📤 Uploading images and posting to Instagram..."):
                            success_count = 0
                            error_count = 0
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            for idx, post_img in enumerate(st.session_state.generated_ig_posts):
                                status_text.text(f"Uploading post {idx + 1} of {len(st.session_state.generated_ig_posts)}...")
                                
                                # Convert PIL Image to bytes
                                img_bytes_io = BytesIO()
                                post_img.save(img_bytes_io, format='JPEG', quality=95)
                                img_bytes_io.seek(0)
                                img_bytes_io.name = f"instagram_post_{idx + 1}.jpg"
                                
                                # Upload to GetLate
                                uploaded_url = upload_image_to_getlate(img_bytes_io, st.session_state.api_key)
                                
                                if uploaded_url:
                                    post_payload = {
                                        "content": ig_caption_tab1 if ig_caption_tab1 else f"Post {idx + 1}",
                                        "platforms": [{
                                            "accountId": st.session_state.ig_account_id,
                                            "mediaItems": [{"url": uploaded_url}]
                                        }],
                                        "timezone": "America/Los_Angeles"
                                    }
                                    
                                    if post_now_tab1:
                                        post_payload["publishNow"] = True
                                    else:
                                        post_payload["scheduledFor"] = schedule_iso_tab1
                                    
                                    response = send_post_to_api(st.session_state.api_key, post_payload)
                                    
                                    if response and response.status_code in [200, 201]:
                                        success_count += 1
                                    else:
                                        error_count += 1
                                else:
                                    error_count += 1
                                
                                progress_bar.progress((idx + 1) / len(st.session_state.generated_ig_posts))
                            
                            status_text.empty()
                            progress_bar.empty()
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            if error_count == 0:
                                st.balloons()
                                st.markdown(f"""
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
                
                # Close button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌ Close Instagram Posting", use_container_width=True):
                    st.session_state.show_ig_posting = False
                    st.rerun()

# ============================================================================
# TAB 2: CTA PODCAST CONTENT
# ============================================================================

with tab2:
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

# ============================================================================
# TAB 3: CREATE CAROUSEL/FEED POST
# ============================================================================

with tab3:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎨 Multi-Platform Post Creator</h1>
            <p style='font-size: 1.1rem; color: #666;'>Upload once, post everywhere</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        st.warning("⚠️ Please enter your GetLate API Key in the sidebar")
    
    # Image upload
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>📤 Upload Your Media</h3>
        </div>
    """, unsafe_allow_html=True)
    
    carousel_images = st.file_uploader(
        "📁 Drop your images here",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        key="carousel_images"
    )
    
    if carousel_images:
        st.success(f"✅ {len(carousel_images)} image(s) uploaded successfully")
    
    st.markdown("---")
    
    # Master content editor
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0; border: 2px solid #667eea;'>
            <h3 style='margin-top: 0; color: #667eea;'>📝 Master Content Editor</h3>
            <p style='color: #4a5568; margin: 0.5rem 0 0 0;'>
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
            placeholder="Write your post content here...",
            key="master_content_input"
        )
        st.session_state.master_content = master_content
    
    with col2:
        st.markdown("**📅 Master Schedule (PDT)**")
        default_date = datetime.now() + timedelta(hours=1)
        master_date = st.date_input("📆 Date", value=default_date)
        master_time = st.time_input("🕐 Time", value=default_date.time())
        
        pdt = pytz.timezone('America/Los_Angeles')
        master_datetime_pdt = pdt.localize(datetime.combine(master_date, master_time))
        master_schedule_iso = master_datetime_pdt.isoformat()
        st.session_state.master_schedule = master_schedule_iso
    
    st.markdown("---")
    
    # Platform selection
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                    padding: 2rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='margin-top: 0;'>🌐 Select Your Platforms</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    enable_instagram = col1.checkbox("📷 **Instagram**")
    enable_linkedin = col2.checkbox("💼 **LinkedIn**")
    enable_facebook = col3.checkbox("👥 **Facebook**")
    enable_twitter = col4.checkbox("🐦 **Twitter**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    platforms_config = []
    
    # INSTAGRAM CONFIGURATION
    if enable_instagram:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #bc1888;'>📷 Instagram Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ig_account_id = st.text_input(
                "🆔 Instagram Account ID",
                key="ig_account_input",
                value=st.session_state.ig_account_id,
                placeholder="Enter your Instagram account ID"
            )
            if ig_account_id != st.session_state.ig_account_id:
                st.session_state.ig_account_id = ig_account_id
                if ig_account_id:
                    save_to_localstorage('ig_account_id', ig_account_id)
            
            if ig_account_id:
                st.caption("✅ Account ID saved permanently")
            
            if 'ig_content_value' not in st.session_state:
                st.session_state.ig_content_value = ""
            
            ig_content = st.text_area(
                "💬 Caption",
                value=st.session_state.ig_content_value,
                height=100,
                key="ig_content_area",
                placeholder="Your Instagram caption..."
            )
            st.session_state.ig_content_value = ig_content
        
        with col2:
            if st.button("📋 Use Master", key="ig_use_master", use_container_width=True):
                st.session_state.ig_content_value = st.session_state.master_content
                st.rerun()
            
            st.markdown("**📅 Schedule**")
            use_master_schedule_ig = st.checkbox("Use master schedule", value=True, key="ig_master_sched")
            
            if not use_master_schedule_ig:
                if 'ig_custom_date' not in st.session_state:
                    st.session_state.ig_custom_date = default_date
                if 'ig_custom_time' not in st.session_state:
                    st.session_state.ig_custom_time = default_date.time()
                
                ig_date = st.date_input("Date", value=st.session_state.ig_custom_date, key="ig_date")
                ig_time = st.time_input("Time (PDT)", value=st.session_state.ig_custom_time, key="ig_time")
                
                st.session_state.ig_custom_date = ig_date
                st.session_state.ig_custom_time = ig_time
                
                ig_schedule = pdt.localize(datetime.combine(ig_date, ig_time)).isoformat()
            else:
                ig_schedule = st.session_state.master_schedule
        
        if ig_account_id:
            media_items = []
            if carousel_images and st.session_state.api_key:
                with st.spinner("📤 Uploading images..."):
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
    
    # LINKEDIN CONFIGURATION
    if enable_linkedin:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #0077b5;'>💼 LinkedIn Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            li_account_id = st.text_input(
                "🆔 LinkedIn Account ID",
                key="li_account_input",
                value=st.session_state.li_account_id
            )
            if li_account_id != st.session_state.li_account_id:
                st.session_state.li_account_id = li_account_id
                if li_account_id:
                    save_to_localstorage('li_account_id', li_account_id)
            
            if li_account_id:
                st.caption("✅ Account ID saved permanently")
            
            if 'li_content_value' not in st.session_state:
                st.session_state.li_content_value = ""
            
            li_content = st.text_area(
                "💬 Post Content",
                value=st.session_state.li_content_value,
                height=100,
                key="li_content_area"
            )
            st.session_state.li_content_value = li_content
        
        with col2:
            if st.button("📋 Use Master", key="li_use_master", use_container_width=True):
                st.session_state.li_content_value = st.session_state.master_content
                st.rerun()
            
            st.markdown("**📅 Schedule**")
            use_master_schedule_li = st.checkbox("Use master schedule", value=True, key="li_master_sched")
            
            if not use_master_schedule_li:
                if 'li_custom_date' not in st.session_state:
                    st.session_state.li_custom_date = default_date
                if 'li_custom_time' not in st.session_state:
                    st.session_state.li_custom_time = default_date.time()
                
                li_date = st.date_input("Date", value=st.session_state.li_custom_date, key="li_date")
                li_time = st.time_input("Time (PDT)", value=st.session_state.li_custom_time, key="li_time")
                
                st.session_state.li_custom_date = li_date
                st.session_state.li_custom_time = li_time
                
                li_schedule = pdt.localize(datetime.combine(li_date, li_time)).isoformat()
            else:
                li_schedule = st.session_state.master_schedule
        
        if li_account_id:
            media_items = []
            if carousel_images and st.session_state.api_key:
                with st.spinner("📤 Uploading images..."):
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
    
    # FACEBOOK CONFIGURATION
    if enable_facebook:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #1877f2 0%, #0c63d4 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #1877f2;'>👥 Facebook Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fb_account_id = st.text_input(
                "🆔 Facebook Account ID",
                key="fb_account_input",
                value=st.session_state.fb_account_id
            )
            if fb_account_id != st.session_state.fb_account_id:
                st.session_state.fb_account_id = fb_account_id
                if fb_account_id:
                    save_to_localstorage('fb_account_id', fb_account_id)
            
            if fb_account_id:
                st.caption("✅ Account ID saved permanently")
            
            if 'fb_content_value' not in st.session_state:
                st.session_state.fb_content_value = ""
            
            fb_content = st.text_area(
                "💬 Post Content",
                value=st.session_state.fb_content_value,
                height=100,
                key="fb_content_area"
            )
            st.session_state.fb_content_value = fb_content
        
        with col2:
            if st.button("📋 Use Master", key="fb_use_master", use_container_width=True):
                st.session_state.fb_content_value = st.session_state.master_content
                st.rerun()
            
            st.markdown("**📅 Schedule**")
            use_master_schedule_fb = st.checkbox("Use master schedule", value=True, key="fb_master_sched")
            
            if not use_master_schedule_fb:
                if 'fb_custom_date' not in st.session_state:
                    st.session_state.fb_custom_date = default_date
                if 'fb_custom_time' not in st.session_state:
                    st.session_state.fb_custom_time = default_date.time()
                
                fb_date = st.date_input("Date", value=st.session_state.fb_custom_date, key="fb_date")
                fb_time = st.time_input("Time (PDT)", value=st.session_state.fb_custom_time, key="fb_time")
                
                st.session_state.fb_custom_date = fb_date
                st.session_state.fb_custom_time = fb_time
                
                fb_schedule = pdt.localize(datetime.combine(fb_date, fb_time)).isoformat()
            else:
                fb_schedule = st.session_state.master_schedule
        
        if fb_account_id:
            media_items = []
            if carousel_images and st.session_state.api_key:
                with st.spinner("📤 Uploading images..."):
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
    
    # TWITTER CONFIGURATION
    if enable_twitter:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #1DA1F2 0%, #0c85d0 100%); 
                        padding: 0.1rem; border-radius: 16px; margin: 1.5rem 0;'>
                <div style='background: white; padding: 2rem; border-radius: 15px;'>
                    <h3 style='margin-top: 0; color: #1DA1F2;'>🐦 Twitter Configuration</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tw_account_id = st.text_input(
                "🆔 Twitter Account ID",
                key="tw_account_input",
                value=st.session_state.tw_account_id
            )
            if tw_account_id != st.session_state.tw_account_id:
                st.session_state.tw_account_id = tw_account_id
                if tw_account_id:
                    save_to_localstorage('tw_account_id', tw_account_id)
            
            if tw_account_id:
                st.caption("✅ Account ID saved permanently")
            
            if 'tw_content_value' not in st.session_state:
                st.session_state.tw_content_value = ""
            
            tw_content = st.text_area(
                "💬 Tweet Content",
                value=st.session_state.tw_content_value,
                height=100,
                max_chars=280,
                key="tw_content_area"
            )
            st.session_state.tw_content_value = tw_content
            
            char_count = len(tw_content)
            if char_count > 280:
                st.error(f"⚠️ {char_count - 280} characters over limit!")
            else:
                st.info(f"✍️ {char_count}/280 characters")
        
        with col2:
            if st.button("📋 Use Master", key="tw_use_master", use_container_width=True):
                st.session_state.tw_content_value = st.session_state.master_content[:280]
                st.rerun()
            
            st.markdown("**📅 Schedule**")
            use_master_schedule_tw = st.checkbox("Use master schedule", value=True, key="tw_master_sched")
            
            if not use_master_schedule_tw:
                if 'tw_custom_date' not in st.session_state:
                    st.session_state.tw_custom_date = default_date
                if 'tw_custom_time' not in st.session_state:
                    st.session_state.tw_custom_time = default_date.time()
                
                tw_date = st.date_input("Date", value=st.session_state.tw_custom_date, key="tw_date")
                tw_time = st.time_input("Time (PDT)", value=st.session_state.tw_custom_time, key="tw_time")
                
                st.session_state.tw_custom_date = tw_date
                st.session_state.tw_custom_time = tw_time
                
                tw_schedule = pdt.localize(datetime.combine(tw_date, tw_time)).isoformat()
            else:
                tw_schedule = st.session_state.master_schedule
        
        if tw_account_id:
            media_items = []
            if carousel_images and st.session_state.api_key:
                with st.spinner("📤 Uploading images..."):
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
    
    # SUBMIT SECTION
    if platforms_config:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
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
                    with st.spinner("📤 Scheduling your posts..."):
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
                                st.success(f"✅ {platform_data['platform']}: Post scheduled!")
                            else:
                                error_count += 1
                                st.error(f"❌ {platform_data['platform']}: Failed")
                            
                            progress_bar.progress((idx + 1) / len(platforms_config))
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if error_count == 0:
                            st.balloons()
                            st.markdown(f"""
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
# TAB 4: SHORT FORM VIDEO
# ============================================================================

with tab4:
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
            <p style='color: #666; margin: 1rem 0 0 0; font-size: 1.1rem;'>We're working hard to bring you short-form video posting!</p>
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
        © 2025 Content Posting Automations
    </p>
</div>
""", unsafe_allow_html=True)import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import zipfile
from io import BytesIO
import math
import requests
import json
from datetime import datetime, timedelta
import pytz
import hashlib

# ============================================================================
# PASSWORD PROTECTION WITH BEAUTIFUL PURPLE GRADIENT LOGIN
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
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .stDeployButton {display: none;}
                
                .main {
                    background: linear-gradient(180deg, #4a148c 0%, #6a1b9a 25%, #8e24aa 50%, #ab47bc 75%, #ce93d8 100%);
                    padding: 0 !important;
                    min-height: 100vh;
                    font-family: 'Poppins', sans-serif;
                    position: relative;
                    overflow: hidden;
                }
                
                .main::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image: 
                        radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.8), transparent),
                        radial-gradient(2px 2px at 60px 70px, rgba(255, 255, 255, 0.6), transparent),
                        radial-gradient(1px 1px at 50px 50px, rgba(255, 255, 255, 0.9), transparent),
                        radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.7), transparent),
                        radial-gradient(2px 2px at 90px 10px, rgba(255, 255, 255, 0.5), transparent);
                    background-size: 200px 200px;
                    animation: stars 20s linear infinite;
                    z-index: 1;
                }
                
                @keyframes stars {
                    from { transform: translateY(0); }
                    to { transform: translateY(-200px); }
                }
                
                .block-container {
                    padding: 0 !important;
                    max-width: 100% !important;
                    position: relative;
                    z-index: 2;
                }
                
                .stTextInput > label {
                    display: none !important;
                }
                
                .stTextInput > div > div {
                    background: transparent !important;
                    border: none !important;
                }
                
                .stTextInput input {
                    background: rgba(255, 255, 255, 0.15) !important;
                    border: 2px solid rgba(255, 255, 255, 0.3) !important;
                    border-radius: 25px !important;
                    color: white !important;
                    padding: 15px 45px 15px 20px !important;
                    font-size: 16px !important;
                    font-family: 'Poppins', sans-serif !important;
                    backdrop-filter: blur(10px) !important;
                    transition: all 0.3s ease !important;
                }
                
                .stTextInput input:focus {
                    border-color: rgba(255, 255, 255, 0.6) !important;
                    box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
                    background: rgba(255, 255, 255, 0.2) !important;
                }
                
                .stTextInput input::placeholder {
                    color: rgba(255, 255, 255, 0.6) !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("""
                <div style='margin-top: 25vh; position: relative; z-index: 10;'>
                    <div style='background: rgba(255, 255, 255, 0.1); 
                                padding: 3rem 2.5rem; 
                                border-radius: 30px; 
                                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                                backdrop-filter: blur(20px);
                                border: 2px solid rgba(255, 255, 255, 0.2);
                                text-align: center;'>
                        <h1 style='color: white; 
                                   margin-bottom: 0.3rem; 
                                   font-size: 2.5rem; 
                                   font-weight: 700;
                                   font-family: Poppins, sans-serif;
                                   text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>
                            Login
                        </h1>
                        <p style='color: rgba(255, 255, 255, 0.8); 
                                  margin-bottom: 2rem; 
                                  font-size: 0.95rem;
                                  font-family: Poppins, sans-serif;'>
                            🔐 Enter password to access Content Posting Automations
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.text_input(
                "Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="🔒 Enter password...",
                label_visibility="collapsed"
            )
            
            st.markdown("""
                <div style='text-align: center; margin-top: 1.5rem;'>
                    <p style='color: rgba(255, 255, 255, 0.7); 
                              font-size: 0.85rem;
                              font-family: Poppins, sans-serif;
                              text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);'>
                        ✨ Protected access • Authorized users only
                    </p>
                </div>
            """, unsafe_allow_html=True)
        return False
        
    elif not st.session_state["password_correct"]:
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .stDeployButton {display: none;}
                
                .main {
                    background: linear-gradient(180deg, #4a148c 0%, #6a1b9a 25%, #8e24aa 50%, #ab47bc 75%, #ce93d8 100%);
                    padding: 0 !important;
                    min-height: 100vh;
                    font-family: 'Poppins', sans-serif;
                    position: relative;
                    overflow: hidden;
                }
                
                .main::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image: 
                        radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.8), transparent),
                        radial-gradient(2px 2px at 60px 70px, rgba(255, 255, 255, 0.6), transparent),
                        radial-gradient(1px 1px at 50px 50px, rgba(255, 255, 255, 0.9), transparent),
                        radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.7), transparent),
                        radial-gradient(2px 2px at 90px 10px, rgba(255, 255, 255, 0.5), transparent);
                    background-size: 200px 200px;
                    animation: stars 20s linear infinite;
                    z-index: 1;
                }
                
                @keyframes stars {
                    from { transform: translateY(0); }
                    to { transform: translateY(-200px); }
                }
                
                .block-container {
                    padding: 0 !important;
                    max-width: 100% !important;
                    position: relative;
                    z-index: 2;
                }
                
                .stTextInput > label {
                    display: none !important;
                }
                
                .stTextInput input {
                    background: rgba(255, 255, 255, 0.15) !important;
                    border: 2px solid rgba(255, 100, 100, 0.5) !important;
                    border-radius: 25px !important;
                    color: white !important;
                    padding: 15px 45px 15px 20px !important;
                    font-size: 16px !important;
                    font-family: 'Poppins', sans-serif !important;
                    backdrop-filter: blur(10px) !important;
                }
                
                .stAlert {
                    background: rgba(255, 100, 100, 0.2) !important;
                    border: 2px solid rgba(255, 100, 100, 0.5) !important;
                    border-radius: 15px !important;
                    color: white !important;
                    backdrop-filter: blur(10px) !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("""
                <div style='margin-top: 25vh; position: relative; z-index: 10;'>
                    <div style='background: rgba(255, 255, 255, 0.1); 
                                padding: 3rem 2.5rem; 
                                border-radius: 30px; 
                                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                                backdrop-filter: blur(20px);
                                border: 2px solid rgba(255, 100, 100, 0.3);
                                text-align: center;
                                animation: shake 0.5s;'>
                        <h1 style='color: white; 
                                   margin-bottom: 0.3rem; 
                                   font-size: 2.5rem; 
                                   font-weight: 700;
                                   font-family: Poppins, sans-serif;
                                   text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>
                            Login
                        </h1>
                        <p style='color: rgba(255, 255, 255, 0.8); 
                                  margin-bottom: 2rem; 
                                  font-size: 0.95rem;
                                  font-family: Poppins, sans-serif;'>
                            🔐 Enter password to access Content Posting Automations
                        </p>
                    </div>
                </div>
                <style>
                    @keyframes shake {
                        0%, 100% { transform: translateX(0); }
                        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                        20%, 40%, 60%, 80% { transform: translateX(5px); }
                    }
                </style>
            """, unsafe_allow_html=True)
            
            st.text_input(
                "Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="🔒 Enter password...",
                label_visibility="collapsed"
            )
            st.error("❌ Incorrect password. Please try again.")
            
            st.markdown("""
                <div style='text-align: center; margin-top: 1.5rem;'>
                    <p style='color: rgba(255, 255, 255, 0.7); 
                              font-size: 0.85rem;
                              font-family: Poppins, sans-serif;
                              text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);'>
                        ✨ Protected access • Authorized users only
                    </p>
                </div>
            """, unsafe_allow_html=True)
        return False
    else:
        return True

# ============================================================================
# LOCALSTORAGE UTILITIES
# ============================================================================

def save_to_localstorage(key, value):
    """Save a value to browser localStorage"""
    js_code = f"""
    <script>
        localStorage.setItem('{key}', '{value}');
    </script>
    """
    st.components.v1.html(js_code, height=0)

def clear_localstorage():
    """Clear all saved data from localStorage"""
    js_code = """
    <script>
        localStorage.removeItem('api_key');
        localStorage.removeItem('ig_account_id');
        localStorage.removeItem('li_account_id');
        localStorage.removeItem('fb_account_id');
        localStorage.removeItem('tw_account_id');
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ============================================================================
# FONT UTILITIES
# ============================================================================

def get_font(size, bold=False):
    """Get Work Sans SemiBold font or fallback to default"""
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

# ============================================================================
# IMAGE PROCESSING FUNCTIONS
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
        instagram_posts.append(create_single_instagram_post(post_images, post_text))
    
    if guest_name.strip():
        instagram_posts.append(create_promotional_post(guest_name, logo_file))
    
    return instagram_posts

def create_single_instagram_post(images, post_text):
    """Create a single Instagram post from 1 or 2 images"""
    POST_SIZE = 1080
    post = Image.new('RGB', (POST_SIZE, POST_SIZE), color='white')
    
    if len(images) == 2:
        img_height = POST_SIZE // 2
        top_img = resize_image_to_exact(images[0], POST_SIZE, img_height)
        bottom_img = resize_image_to_exact(images[1], POST_SIZE, img_height)
        
        text_parts = split_text_for_post(post_text)
        if len(text_parts) >= 1 and text_parts[0].strip():
            top_img = add_text_overlay(top_img, text_parts[0])
        if len(text_parts) >= 2 and text_parts[1].strip():
            bottom_img = add_text_overlay(bottom_img, text_parts[1])
        
        post.paste(top_img, (0, 0))
        post.paste(bottom_img, (0, POST_SIZE // 2))
    else:
        img = resize_image_to_exact(images[0], POST_SIZE, POST_SIZE)
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
    main_font = get_font(36, bold=True)
    wrapped_text = wrap_text(main_text, main_font, POST_SIZE - 120)
    
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=main_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    logo_height = 0
    logo = None
    if logo_file:
        try:
            logo = Image.open(logo_file)
            logo.thumbnail((200, 200), Image.Resampling.LANCZOS)
            logo_height = logo.height + 40
        except:
            pass
    
    available_height = POST_SIZE - logo_height
    text_y = (available_height - text_height) // 2 + (logo_height if logo else 0)
    text_x = (POST_SIZE - text_width) // 2
    
    draw.multiline_text((text_x + 3, text_y + 3), wrapped_text, fill='black', font=main_font, align='center')
    draw.multiline_text((text_x, text_y), wrapped_text, fill='#F4DB7D', font=main_font, align='center')
    
    if logo:
        logo_x = (POST_SIZE - logo.width) // 2
        post.paste(logo, (logo_x, 60), logo if logo.mode == 'RGBA' else None)
    
    return post

def split_text_for_post(text):
    """Split text into two roughly equal parts"""
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
    
    return [" ".join(words[:break_point]), " ".join(words[break_point:])]

def add_text_overlay(img, text):
    """Add white text with black shadow overlay"""
    if not text.strip():
        return img
    
    img_with_text = img.copy()
    if img_with_text.mode != 'RGB':
        img_with_text = img_with_text.convert('RGB')
    
    draw = ImageDraw.Draw(img_with_text)
    img_width, img_height = img.size
    
    font_size = max(24, min(44, img_width // 25))
    font = get_font(font_size)
    wrapped_text = wrap_text(text, font, img_width - 60)
    
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (img_width - text_width) // 2
    text_y = img_height - text_height - 25
    
    if text_height > img_height * 0.3:
        text_y = max(img_height * 0.7, img_height - img_height * 0.3 - 25)
    
    text_x = max(30, min(text_x, img_width - text_width - 30))
    
    bg_coords = [
        max(0, text_x - 15),
        max(0, text_y - 15),
        min(img_width, text_x + text_width + 15),
        min(img_height, text_y + text_height + 15)
    ]
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(bg_coords, fill=(0, 0, 0, 120))
    
    img_with_text = Image.alpha_composite(img_with_text.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img_with_text)
    
    draw.multiline_text((text_x + 2, text_y + 2), wrapped_text, fill='black', font=font, align='center')
    draw.multiline_text((text_x, text_y), wrapped_text, fill='white', font=font, align='center')
    
    return img_with_text

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
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
    """Resize image to exact dimensions"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        new_height = target_height
        new_width = int(target_height * img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - target_width) // 2
        return resized.crop((left, 0, left + target_width, target_height))
    else:
        new_width = target_width
        new_height = int(target_width / img_ratio)
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - target_height) // 2
        return resized.crop((0, top, target_width, top + target_height))

def pil_to_bytes(img):
    """Convert PIL Image to bytes"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=95, optimize=True)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def create_zip_from_posts(instagram_posts, original_images=None):
    """Create zip file with Instagram posts"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, post_img in enumerate(instagram_posts):
            img_bytes = pil_to_bytes(post_img)
            zip_file.writestr(f"instagram_posts/post_{i+1}.jpg", img_bytes)
        
        if original_images:
            for i, img_file in enumerate(original_images):
                try:
                    img = Image.open(img_file)
                    img_bytes = pil_to_bytes(img)
                    zip_file.writestr(f"original_screenshots/screenshot_{i+1}.jpg", img_bytes)
                except:
                    pass
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# ============================================================================
# API FUNCTIONS
# ============================================================================

def upload_image_to_getlate(image_file, api_key):
    """Upload image to GetLate"""
    try:
        image_file.seek(0)
        files = {'files': (image_file.name, image_file, 'image/jpeg')}
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.post("https://getlate.dev/api/v1/media", headers=headers, files=files)
        
        if response.status_code in [200, 201]:
            return response.json()['files'][0]['url']
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def send_post_to_api(api_key, post_data):
    """Send post to GetLate API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        return requests.post("https://getlate.dev/api/v1/posts", headers=headers, json=post_data)
    except Exception as e:
        return None

def build_post_payload(content, scheduled_time, timezone, platforms_config):
    """Build API payload"""
    payload = {
        "content": content,
        "scheduledFor": scheduled_time,
        "timezone": timezone,
        "platforms": []
    }
    
    for platform_data in platforms_config:
        payload["platforms"].append({
            "accountId": platform_data["accountId"],
            "mediaItems": platform_data.get("mediaItems", [])
        })
    
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

if not check_password():
    st.stop()

# Complete CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    
    .main { background: #f5f7fa; padding: 0 !important; }
    .block-container { 
        padding: 2rem 3rem !important; 
        max-width: 1400px !important; 
        margin: 0 auto !important; 
    }
    
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
        transition: all 0.3s ease; 
    }
    
    .stTabs [data-baseweb="tab"]:hover { 
        background: #f5f7fa; 
        color: #667eea; 
    }
    
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; 
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3); 
    }
    
    .stTabs [aria-selected="true"] * { color: #ffffff !important; }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }

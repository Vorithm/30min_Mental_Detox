import streamlit as st
import pandas as pd
import time
import random
# --- Config ---
st.set_page_config(page_title="30min Mental Detox", page_icon="🌱", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        q = pd.read_csv("questions_dataset.csv")
        d = pd.read_csv("mental_detox_dataset.csv")
        # Clean columns and options
        q.columns = [c.strip() for c in q.columns]
        d.columns = [c.strip().lower() for c in d.columns]
        q["Options"] = q["Option"].apply(lambda x: [i.strip() for i in str(x).split("|")] if pd.notna(x) else [])
        return q, d
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Make sure 'questions_dataset.csv' and 'mental_detox_dataset.csv' are in the same folder as your script.")
        return pd.DataFrame(), pd.DataFrame()

questions_df, detox_df = load_data()

# --- Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "language" not in st.session_state:
    st.session_state.language = ""
if "issue" not in st.session_state:
    st.session_state.issue = ""
if "issue_icon" not in st.session_state:
    st.session_state.issue_icon = ""
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "content_index" not in st.session_state:
    st.session_state.content_index = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "released_thought" not in st.session_state:
    st.session_state.released_thought = ""
if "released_text" not in st.session_state:
    st.session_state.released_text = ""
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# --- Page 1: Welcome & Inputs ---
if st.session_state.step == 1:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {background-color: #ffffff !important;}
        .main { background-color: #ffffff !important; }
        .big-title {font-size: 2.7rem; font-weight: bold; margin-bottom: 8px; color: black;}
        .legend {font-size: 1.22rem; margin-bottom: 24px; color: black;}
        .stTextInput>div>input, .stSelectbox>div>div {background: #ffffff; color: #000; border-radius: 10px; border: 1px solid #000;}
        div.stButton > button {background-color: #191b22 !important; color: white !important; font-weight: 700 !important;
            border-radius: 12px !important; padding: 12px 22px !important; border: none !important;}
        .stSelectbox > div > div {background: #191b22 !important; color: #fff !important; border-radius: 10px !important;
        border: 1px solid #000 !important;}
        .stSelectbox [data-testid="stMarkdownContainer"] {color: #222 !important;}
    </style>
    """, unsafe_allow_html=True)

    colL, colR = st.columns([1.2, 2])
    with colL:
        st.image("Welcome.jpg", use_container_width=True)
    with colR:
        st.markdown("""<div style="display: flex; gap: 12px; align-items: center; margin-top:20px;">
        <span style="font-size:2rem;"><span class="big-title ">Your Inner Healing Space</span><span style="font-size:2rem;">🌿</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="legend">
        This is your space to relax and feel peaceful.<br>
        Take a deep breath… let go of stress.<br>
        Here, you will find calm thoughts, positive energy, and gentle guidance.<br>
        Remember — peace is already inside you. <span style="font-size:1.6rem;">🌙</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.7rem; font-weight: bold; color: #FFA07A;">Begin Your Healing Journey</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 1.22rem; color: black;">What should we call you during this sacred time?</div>', unsafe_allow_html=True)
        name = st.text_input("", value=st.session_state.name, key="name_input", placeholder="Enter your sacred name...")
        if name.strip():
            st.session_state.name = name
            language = st.selectbox("Select language", ["English", "Hindi"], index=None, placeholder="Choose language...", key="lang_input")
            if language:
                st.session_state.language = language
                st.session_state.step = 2
                st.rerun()

# --- Page 2: Select Issue ---
elif st.session_state.step == 2:
    st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
    .main { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
    .welcome-text {
        font-size: 1.9rem; color: #2B2B2B; margin-bottom: 10px; text-align: center;}
    .question-text {
        font-size: 2rem; font-weight: 700; color: #000000; margin-bottom: 30px; text-align: center;}
    div.stButton > button {
        width: 300px !important;  
        height: 102px !important;
        border-radius: 44px !important;
        background: #f5d0ba!important;
        border: 2px solid black !important;
        box-shadow: 0 4px 18px rgba(211,138,219,0.11);
        color: #000000 !important; 
        font-size: 1.3rem;
        font-weight: 600 !important;
        margin: 14px auto 14px auto;
        letter-spacing: 0.04em;
        padding: 0 !important;
        transition: all 0.25s;
        white-space: nowrap !important;  
        overflow: hidden !important;  
        text-overflow: ellipsis !important;}
    div.stButton > button:hover {
        background: #cfe9fa !important;
        color: #000000 !important;  
        transform: scale(1.06);
        box-shadow: 0 8px 22px rgba(195,177,225,0.21);}
    .bottom-text {
        font-size: 1.20rem; 
        color: black; 
        margin-top: 45px; 
        text-align: center; 
        font-style: italic;}
</style>
""", unsafe_allow_html=True)
    
    st.markdown(
        f'<div class="welcome-text">Welcome, {st.session_state.name} 🙏<br>Let\'s understand how your heart is feeling today</div>', 
        unsafe_allow_html=True)
    st.markdown('<div class="question-text">How are you feeling right now?</div>', unsafe_allow_html=True)
    issues = [
        ("😡", "Anger"), 
        ("🌱", "Life Transitions"), 
        ("😔", "Depression"),
        ("😕", "Fear"), 
        ("😢", "Sadness"),
        ("🤔", "Overthinking"),
        ("🧍", "Loneliness"),
        ("😞", "Hopelessness"),
        ("😟", "Self-Doubt"),   
    ]
    for i in range(0, len(issues), 3):
        cols = st.columns(3)          
        for j in range(3):
            if i + j < len(issues):
                with cols[j]:
                    emoji, issue_name = issues[i + j]
                    if st.button(f"{emoji}\n**{issue_name}**", key=f"pill_{issue_name}"):
                        st.session_state.issue       = issue_name
                        st.session_state.issue_icon  = emoji
                        st.session_state.answers     = {}
                        st.session_state.step        = 3
                        st.rerun()
    st.markdown(
        f'<div class="bottom-text" >Remember, dear {st.session_state.name}, every master was once a disaster. Every pro was once an amateur. You are exactly where you need to be on your journey of growth.</div>', 
        unsafe_allow_html=True)


# --- Page 3: Questions ---
elif st.session_state.step == 3:
    st.markdown("""
    <style>
       [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .main { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .progress-bar{ text-align:center; margin-bottom:8px; font-size:1.09rem; color: #2B2B2B; font-weight:700; }
        .heart-icon{display:flex; justify-content:center; align-items:center; margin-bottom:10px; }
        .heart-bg{ background:linear-gradient(135deg,#d175fa 0%,#f7a7dc 100%); border-radius:50%;
               width:54px; height:54px; display:flex; align-items:center; justify-content:center; }
        .question-main{ text-align:center; font-size:1.40rem; font-weight:600; margin-bottom:18px; color:#2B2B2B; }
        .stRadio > div{ display:grid !important;grid-template-columns:1fr 1fr;gap:15px 17px;margin:0 auto !important; }
        .stRadio label p { color:black !important;font-size:1.11rem !important;margin:0;font-weight:normal !important; }
        .stRadio label{ background:#f5f5fa !important;border:1.8px solid black !important;border-radius:14px;
               padding:14px 10px !important;font-size:1.11rem !important;font-weight:normal !important;
               cursor:pointer;transition:all .18s;text-align:center;display:flex;align-items:center;
               min-height:50px !important; }
        .stRadio label:hover { transform:translateY(-3px);box-shadow:0 2px 8px rgba(171,60,255,.13); }
        .stRadio label[aria-checked="true"]{
           border:2.5px solid #d175fa !important;background:#f7e6fc !important;color:#cfe9fa !important;
             box-shadow:0 6px 16px #edd2fa77; }
        .stRadio input  { display:none !important; }
        div.stButton > button  {  background: #f5d0ba !important; border: 2px solid black !important;
            box-shadow: 0 4px 18px rgba(211,138,219,0.11);color: #000000 !important; color:black !important;
            font-size:1.11rem !important;font-weight:600 !important;border-radius:32px !important;
            box-shadow: 0 8px 22px rgba(195,177,225,0.21); !important;display:block;width:220px;margin:16px auto 0;
             padding:14px 0; }
        div.stButton > button:hover      {background: #cfe9fa !important; color: #000000 !important;  
                         transform: scale(1.06); box-shadow: 0 8px 22px rgba(195,177,225,0.21);
        .stAlert p              {color:black !important; text-align:center; }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='centered'><h2 style='text-align:center;color:black;'>Thanks {st.session_state.name}, A few quick questions…</h2>"
        f"<p style='font-size:1.5rem;text-align:center;color:black;'>Mood selected: "
        f"{st.session_state.issue_icon} {st.session_state.issue}</p></div>",
        unsafe_allow_html=True)

    # --- Filter the questions for the selected issue/language ---
    issue_to_filter    = st.session_state.issue.strip().lower()
    language_to_filter = st.session_state.language.strip().lower()

    qdf = questions_df[
        (questions_df["Issue"].str.strip().str.lower()   == issue_to_filter) &
        (questions_df["Language"].str.strip().str.lower()== language_to_filter)
    ].head(3)

    if qdf.empty:
        st.warning("No questions found for this issue in the selected language.")
        _, back_center, _ = st.columns([1,2,1])
        with back_center:
            if st.button("⬅  Back to issue list", key="back_no_question"):
                st.session_state.step            = 2
                st.session_state.current_question= 0
                st.session_state.answers         = {}
                st.rerun()
        st.stop()  
    total_questions = len(qdf)
    if st.session_state.current_question < total_questions:
        row          = qdf.iloc[st.session_state.current_question]
        question_key = f"q_{row.name}"
        options      = row["Options"]

        def on_option_change():
            st.session_state.answers[question_key] = st.session_state[question_key]
        st.markdown(f'<div class="progress-bar">Question {st.session_state.current_question+1} of {total_questions}</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="heart-icon"><div class="heart-bg"><span style="font-size:2rem;color:#fff;">&#10084;&#65039;</span></div></div>',
            unsafe_allow_html=True)
        st.markdown(f'<div class="question-main">{row["Question"]}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.radio("", options, index=None, key=question_key,
                     label_visibility="collapsed", on_change=on_option_change)

        _, nav_center, _ = st.columns([1,2,1])
        with nav_center:
            back_col, next_col = st.columns(2)

            with back_col:
                if st.button("⬅  Back", key="back3"):
                    st.session_state.step             = 2
                    st.session_state.current_question = 0
                    st.session_state.answers          = {}
                    st.rerun()

            with next_col:
                if st.button("Next ➡", key=f"next_{st.session_state.current_question}"):
                    if question_key in st.session_state.answers and st.session_state.answers[question_key] is not None:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.warning("Please select an option before proceeding.")
    else:
        st.session_state.step = 4
        st.rerun()


# -----Page 4: Wisdom & Guidance -----
elif st.session_state.step == 4:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .main { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .wisdom-title{font-size:2.3rem;font-weight:700;text-align:center;color:#2c2d3c;margin-top:24px;margin-bottom:5px;}
        .wisdom-sub  {text-align:center;color:black ;font-size:2.09rem;margin-bottom:28px;}
        div.stButton>button{
            padding:10px 10px!important;
            border-radius:30px!important;
            font-size:1.1rem!important;
            font-weight:800;
            background: #f5d0ba !important;
            border: 2px solid black !important;
            box-shadow: 0 4px 18px rgba(211,138,219,0.11);
            color: #000000 !important; 
            transition:transform .2s,box-shadow .2s;
        }
        div.stButton>button:hover{
            transform:translateY(-2px);
            box-shadow:0 5px 14px rgba(146,58,240,.14),0 2px 8px  #2B2B2B;
        }
        .wisdom-card{background:linear-gradient(92deg,#fef6e5 50%,#f7fafc 50%);
                     border-radius:20px;box-shadow:0 2px 15px #ebdda777;
                     padding:10px 10px 10px; margin:8px 0 20px;position:relative;}
        .wisdom-card .star{font-size:1.18rem;background:#ffd085;color:#dc9a07;border-radius:50%;
             padding:6px 13px;position:absolute;left:17px;top:16px;font-weight:bold;box-shadow:0 2px 8px #ffdca044;}
        .wisdom-card blockquote{font-size:1.13rem;font-weight:700;color:#000;margin:18px 0 16px 48px;font-style:italic;line-height:1.5;}
        .wisdom-ref{color:#c96e29;font-size:1rem;font-weight:700;margin-left:48px;margin-bottom:9px;display:block;}
        .wisdom-meaning{background:#fffbe3;padding:11px 16px;border-radius:10px;font-size:1.01rem;color:#4b4522;
             margin:8px 0 0 48px;font-weight:500;box-shadow:0 1px 2px #e7e8ea24;}
        .growth-card{background:#fff;border-radius:14px;padding:23px 22px;margin-top:36px;
                     box-shadow:0 1px 7px #ece6f5a0;text-align:center;font-size:1.13rem;color:#be2d6e;}
        .growth-card .heart-icon{font-size:2rem;color:#be2d6e;margin-bottom:5px;display:block;}
        .wisdom-tab-content{max-width:860px;margin:0 auto;}
        .video-container { text-align: center; margin: 0 auto; width: 400px; height: 200px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="wisdom-title">Wisdom for Your Soul, {st.session_state.name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="wisdom-sub">Ancient wisdom and modern guidance for healing</div>', unsafe_allow_html=True)

    if "content_index" not in st.session_state:
        st.session_state.content_index = 0
    if "show_prompt" not in st.session_state:
        st.session_state.show_prompt = False

    # Filter dataframe for the selected issue and language
    df = detox_df[
        (detox_df["issue"].str.strip().str.lower() == st.session_state.issue.strip().lower()) &
        (detox_df["language"].str.strip().str.lower() == st.session_state.language.strip().lower())
    ]

    st.markdown('<div class="wisdom-tab-content">', unsafe_allow_html=True)

    # Display Sacred Wisdom quotes (first part of merged content)
    if df.empty:
        sample = [("Perform your duty equipoised, abandoning all attachment to success or failure.",
                   "Bhagavad Gita 2.48",
                   "Anxiety comes from attachment to outcomes. Focus on the present moment and your duty."),
                  ("One who is steady in both pleasure and pain, and treats gold and stone equally.",
                   "Bhagavad Gita 14.24",
                   "Peace comes from equanimity. All experiences are temporary.")]
        for q, ref, tip in sample:
            st.markdown(f"""
                <div class="wisdom-card">
                    <span class="star">★</span>
                    <blockquote>{q}</blockquote>
                    <span class="wisdom-ref">— {ref}</span>
                    <div class="wisdom-meaning"><b>Meaning:</b> {tip}</div>
                </div>""", unsafe_allow_html=True)
    else:
        # Show 2 quotes at a time, cycling through
        num_quotes = 2
        total_items = len(df) * 2  # Assuming each row has quotes and links; adjust if needed
        start_idx = (st.session_state.content_index * num_quotes) % len(df)
        end_idx = start_idx + num_quotes
        if end_idx > len(df):
            selected_df = pd.concat([df.iloc[start_idx:], df.iloc[:end_idx - len(df)]])
        else:
            selected_df = df.iloc[start_idx:end_idx]
        for _, r in selected_df.iterrows():
            st.markdown(f"""
                <div class="wisdom-card">
                    <span class="star">★</span>
                    <blockquote>{r['quote']}</blockquote>
                    <span class="wisdom-ref">— {r.get('refrence','')}</span>
                    <div class="wisdom-meaning"><b>Meaning:</b> {r.get('tips','')}</div>
                </div>""", unsafe_allow_html=True)

    # Merged Guided Teachings content (videos/audio)
    if not df.empty:
        import re
        row = df.iloc[st.session_state.content_index % len(df)]
        links_str = str(row.get("links", ""))
        if links_str.strip():
            for link in links_str.split(','):
                link = link.strip()
                if not link:
                    continue
                if "youtube" in link.lower() or "youtu.be" in link.lower():
                    m = re.search(r'(?:youtube(?:-nocookie)?\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?|shorts)/|\S*?[?&]v=)|youtu\.be/)([a-zA-Z0-9_-]{11})', link)
                    if m:
                        yt_id = m.group(1)
                        responsive_html = (
                            '<div class="responsive-video" style="position: relative; width: 100%; max-width: 800px; margin: 0 auto; text-align: center;">'
                            '<iframe '
                            'src="https://www.youtube.com/embed/' + yt_id + '" '
                            'frameborder="0" allowfullscreen '
                            'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
                            '</iframe>'
                            '<div class="aspect-ratio" style="padding-top: 56.25%;"></div>'  # Maintains 16:9 aspect ratio
                            '</div>'
                            '<style>'
                            '@media (max-width: 600px) {  /* Target mobile phones */'
                            '  .responsive-video { '
                            '    height: 100vh;  /* Fill full viewport height on mobile */'
                            '  }'
                            '  .responsive-video .aspect-ratio { '
                            '    padding-top: 0 !important;  /* Allow vertical fill */'
                            '  }'
                            '  .responsive-video iframe {'
                            '    height: 100vh !important;  /* Force vertical fill without rotation */'
                            '    object-fit: cover;  /* Zoom/crop to fill screen */'
                            '  }'
                            '}'
                            '</style>'
                        )
                        st.markdown(responsive_html, unsafe_allow_html=True)
                    else:
                        st.warning(f"Invalid YouTube link: {link}")
        else:
            st.warning("No video or audio links found for this selection.")

    st.markdown(f"""
        <div class="growth-card">
            <span class="heart-icon">❤</span>
            "Remember, dear {st.session_state.name}, every master was once a disaster.
            Every pro was once an amateur. You are exactly where you need to be on your journey of growth."
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    nav_sp_l, nav_col1, nav_col2, nav_sp_r = st.columns([3,1,1,3])
    with nav_col1:
        if st.button("Show me other option", key="btn_other"):
            st.session_state.content_index += 1
            st.session_state.show_prompt = True
            st.rerun()
    with nav_col2:
        if st.button("Continue to Next Step", key="btn_next"):
            st.session_state.step = 5
            st.rerun()

# --- Page 5: Meditation Timer ---
elif st.session_state.step == 5:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"]{background:#ffffff!important }
        .breath-circle{width:180px;height:180px;border-radius:50%;
                      background:radial-gradient(circle,#a7f3d0 60%,#57e6b0 100%);
                      margin:24px auto;text-align:center;line-height:180px;
                      font-size:30px;color:#064e3b;font-weight:bold}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state variables to avoid AttributeError
    if 'meditation_start' not in st.session_state:
        st.session_state.meditation_start = None
    if 'meditation_time' not in st.session_state:
        st.session_state.meditation_time = 0
    if 'breath_phase_index' not in st.session_state:
        st.session_state.breath_phase_index = 0  # Tracks current phase (0: Inhale, 1: Hold, etc.)
    if 'phase_elapsed' not in st.session_state:
        st.session_state.phase_elapsed = 0  # Seconds in current phase
    
    colL, colR = st.columns([1.2, 2])
    with colL:
        st.image("Meditation.jpg", use_container_width=True)
    with colR:
        st.markdown("<h2 style='color:black'>✨ Find Your Calm ✨</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="legend" style="color:black">
            Close your eyes. Breathe in slowly… breathe out gently.
            Let your thoughts settle like still water. In this moment, nothing is missing.
            You are calm. You are complete. 🌸 🌙
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        breath_placeholder = st.empty()  
        breath_placeholder.markdown("<div class='breath-circle'>Inhale</div>", unsafe_allow_html=True)

        timer_placeholder = st.empty()
        colS, colT = st.columns(2)
        with colS:
            if st.button("Start Meditation"):
                if st.session_state.meditation_start is None:
                    st.session_state.meditation_start = time.time()
                    st.session_state.breath_phase_index = 0
                    st.session_state.phase_elapsed = 0
        with colT:
            if st.button("Stop Meditation"):
                if st.session_state.meditation_start is not None:
                    st.session_state.meditation_time = int(time.time() - st.session_state.meditation_start)
                    st.session_state.meditation_start = None
                    st.session_state.breath_phase_index = 0
                    st.session_state.phase_elapsed = 0

        if st.session_state.meditation_start is not None:
            st.audio("https://www.soundjay.com/nature/sounds/river-1.mp3", autoplay=True, loop=True)
            
            elapsed = int(time.time() - st.session_state.meditation_start)
            mins, secs = divmod(elapsed, 60)
            timer_placeholder.markdown(
                f"<h3 style='text-align:center;color:black'>Meditation Time: {mins:02d}:{secs:02d}</h3>",
                unsafe_allow_html=True,
            )
            
            phases = ["Inhale", "Hold", "Exhale", "Hold"]
            phase_durations = [4, 4, 4, 4]  
            
            current_phase = phases[st.session_state.breath_phase_index]
            breath_placeholder.markdown(f"<div class='breath-circle'>{current_phase}</div>", unsafe_allow_html=True)
            
            st.session_state.phase_elapsed += 1
            if st.session_state.phase_elapsed >= phase_durations[st.session_state.breath_phase_index]:
                st.session_state.phase_elapsed = 0
                st.session_state.breath_phase_index = (st.session_state.breath_phase_index + 1) % len(phases)   
            time.sleep(1)
            st.rerun()

        if st.button("Next"):
            st.session_state.step = 6
            st.rerun()

# --- Page 6: Release and Transform, with Ritual Animation ---
elif st.session_state.step == 6:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
    .main { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .stTextArea textarea {
            border: 2px solid #d7a1f9 !important;
            border-radius: 11px !important;
            background-color: #fff !important;  
            color: #222 !important;            
            font-size: 1.12rem;
            padding: 20px; !important;
            min-height: 120px;
        }
        .release-title { text-align: center; font-size: 2.2rem; font-weight: 700; color: black; margin-top: 40px; margin-bottom: 4px; }
        .release-sub { text-align: center; font-size: 1.5rem; color: #2B2B2B; margin-bottom: 20px; }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff !important; border-radius: 20px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); padding: 30px; border: none !important;
        }
        .card-label { font-size: 1.2rem; font-weight: 600; color: #6a1b9a; margin-bottom: 10px; text-align: left; }
        .stTextArea textarea {
            border: 2px solid #d7a1f9 !important; border-radius: 10px !important; background: #f9f9f9 !important; min-height: 120px;
        }
        .stButton button { border-radius: 10px; padding: 10px 20px; font-weight: 600; border: none; }
        .stButton button[kind="secondary"] { background: #e0e0e0; color: #333; }
        .stButton button[kind="primary"] { background: #ff9800; color: white; }
        .release-quote { text-align: center; font-size: 1.3rem; font-style: italic; color: black; margin-top: 20px; }
        .burn-box, .trans-box {
            background: #f7f6fc; border-radius: 18px; box-shadow: 0 3px 18px #d2dcf855;
            padding: 38px 28px; text-align: center; margin: 24px auto 20px auto; max-width: 530px;
        }
        .burn-icon, .trans-icon { font-size: 2.6rem; color: #ff8c23; font-weight: bold; }
        .burn-msg, .trans-msg { color: #24846e; font-size: 1.33rem; font-weight: 600; margin-top: 24px; }
        .ritual-box {
            background: #ede7fa; border-radius: 15px; padding: 20px 22px; margin: 38px auto 25px auto; max-width: 730px;
            font-size: 1.15rem; color: #24846e; text-align: left; box-shadow: 0 1px 7px #e8eafc23;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='release-title'>Release and Transform, {st.session_state.name}</div>", unsafe_allow_html=True)
    st.markdown("<div class='release-sub'>Write down your negative thoughts, worries, and burdens. Then watch them transform through<br>the sacred fire of release.</div>", unsafe_allow_html=True)

    # State initialization for transformation flow
    if "ritual_stage" not in st.session_state:
        st.session_state.ritual_stage = "write"

    if st.session_state.ritual_stage == "write":
        left, centre, right = st.columns([2,5,2])
        with centre:
            with st.container(border=True):
                st.markdown("<div class='card-label'>🖊️ Your Sacred Writing Space</div>", unsafe_allow_html=True)
                released_text = st.text_area(
                    "Pour out your heart here…",
                    value=st.session_state.get("released_text", ""),
                    height=200, width=800, key="release_text_input", label_visibility="collapsed"
                )
                st.session_state.released_text = released_text
                c1, c2, _ = st.columns([1,2,4])
                with c1:
                    if st.button("Clear", key="clear_release", type="secondary"):
                        st.session_state.released_text = ""
                        st.rerun()
                with c2:
                    if st.button("🔥 Burn & Release", key="burn_release", type="primary"):
                        if st.session_state.released_text.strip():
                            st.session_state.transform_msg = st.session_state.released_text
                            st.session_state.released_text = ""
                            st.session_state.ritual_stage = "burning"
                            st.rerun()
                        else:
                            st.warning("Please write something to release.")
        st.markdown("<div class='release-quote'>“What we resist persists. What we release, finds peace.”</div>", unsafe_allow_html=True)

    elif st.session_state.ritual_stage == "burning":
        # --- Burning Animation ---
        left, centre, right = st.columns([2,5,2])
        with centre:
            st.markdown("""
                <div class='burn-box'>
                    <div style="display:flex; justify-content:center; align-items:center; gap:25px;">
                        <span style="font-size:1.2rem; color:#ae97fe;">{}</span>
                        <span class='burn-icon'>🔥</span>
                    </div>
                    <div class='burn-msg'>Burning...</div>
                </div>
            """.format(st.session_state.transform_msg), unsafe_allow_html=True)
        st.markdown("""
            <div class='ritual-box'>
                <span>🔄</span>
                This is a symbolic ritual of release. As your words burn away, imagine your emotional burdens transforming into wisdom, strength, and inner peace.
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5) 
        st.session_state.ritual_stage = "transformed"
        st.rerun()

    elif st.session_state.ritual_stage == "transformed":
        left, centre, right = st.columns([2,5,2])
        with centre:
            st.markdown("""
                <div class='trans-box'>
                    <div style="display:flex; justify-content:center; align-items:center; gap:25px;">
                        <span style="font-size:1.2rem; color:#ae97fe;">{}</span>
                        <span class='trans-icon'>✨</span>
                    </div>
                    <div class='trans-msg'>Transformed into light ✨</div>
                </div>
            """.format(st.session_state.transform_msg), unsafe_allow_html=True)
        st.markdown("""
            <div class='ritual-box'>
                <span>🔄</span>
                This is a symbolic ritual of release. As your words burn away, imagine your emotional burdens transforming into wisdom, strength, and inner peace.
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.2)  
        st.session_state.step = 7
        st.session_state.ritual_stage = "done"
        st.rerun()

# --- Page 7: Transformation Complete / Affirmation ---
elif st.session_state.step == 7:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(90deg, #f9c16d 60%, #e9b083 100%) !important;  /* Orange gradient like ss 4 */
        }
        .complete-title { text-align: center; font-size: 2.65rem; font-weight: 700; color: #fffbe9; margin-top: 40px; margin-bottom: 4px; }
        .complete-sub { text-align: center; font-size: 1.25rem; color: black; margin-bottom: 28px; }
        .affirm-card {
            background: rgba(255,255,255,0.08); border-radius: 27px; box-shadow: 0 6px 18px #fad79e33;
            padding: 48px 32px 32px 32px; margin: 0 auto 34px auto; max-width: 730px; min-width: 320px; text-align: center;
        }
        .affirm-icon { font-size: 2.2rem; color: #f7b434; font-weight: bold; margin-bottom: 8px; }
        .affirm-label { font-size: 2.1rem; color: #fffbe6; font-weight: 700; margin-bottom: 12px; }
        .affirm-quote { font-size: 1.22rem; font-style: italic; color: black; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='complete-title'>Transformation Complete, {st.session_state.name}</div>", unsafe_allow_html=True)
    st.markdown("<div class='complete-sub'>Your thoughts have been transformed into wisdom. You are now lighter, freer, and more at peace.</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='affirm-card'>
            <div class='affirm-icon'>✨</div>
            <div class='affirm-label'>Sacred Affirmation</div>
            <div class='affirm-quote'>
                "I release what no longer serves me. I am open to peace, love, and new possibilities. My heart is light, my mind is clear, and my spirit is free."
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    left_spc, btn1_col, gap, btn2_col, right_spc = st.columns([3,2,1,2,3])

    with btn1_col:
        if st.button("❤️ Complete Your Journey", key="complete_journey"):
            st.session_state.step = 8         
            st.rerun()

    with btn2_col:
        if st.button("🔁 Release More Thoughts", key="release_more"):
            st.session_state.step = 6
            st.session_state.ritual_stage = "write"
            st.rerun()

# -------Last Page: Summary -------
elif st.session_state.step == 8:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
    .main { background: linear-gradient(to bottom, #92B9B6 0%, #E9D5B3 100%) !important; }
        .journey-title { text-align:center;font-size:2.45rem;font-weight:600;color:#3539a2;margin-top:24px; }
        .journey-sub { text-align:center;font-size:1.35rem;color:black; margin-bottom:44px;}
        .summary-cards { display: flex; gap:28px; justify-content:center; margin-bottom:48px; }
        .summary-card {background: #fff; border-radius:20px; box-shadow: 0 2px 18px #d1e8e270; width: 270px;
            min-width:180px; padding: 38px 10px 24px 10px; text-align:center; display:flex; flex-direction:column; align-items:center;}
        .card-icon { font-size:2.5rem;margin-bottom:18px;}
        .card-label {font-weight:800; font-size:1.20rem; margin-bottom:7px;color:#252755;}
        .card-value-purple { color:#9249d7; font-size:1.6rem;font-weight:700;margin-bottom:5px;}
        .card-value-orange {background:linear-gradient(90deg,#ffa000,#ff6530); color:#fff;font-weight:700; font-size:1.1rem; border-radius:24px;padding:8px 24px;margin-bottom:8px;}
        .card-value-green { color:#19a87b; font-size:1.7rem;font-weight:700;margin-bottom:7px;}
        .journey-section {background: #ffeef6; border-radius: 20px; padding: 32px 22px; margin: 32px auto;
            max-width: 900px; box-shadow: 0 2px 18px #eddbfa1f; text-align: center;}
        .journey-section h2 {font-size:1.75rem; color:#2b355f;}
        .journey-list { background: #f5fefa; border-radius: 16px; padding: 6px 30px; margin: 22px auto 40px auto; max-width: 900px;
            box-shadow: 0 2px 6px #e7f5ea1b;}
        .journey-list-item {background: #e6faee; border-radius:8px; margin-bottom:13px; font-size:1.14rem;
            padding:13px 14px; color:#269d6b; display: flex; align-items:center;}
        .journey-list-item .check { font-size:1.3rem; margin-right:10px; }
        .affirmation-section {background: linear-gradient(90deg,#f5e1fa 95%,#f8eed8 100%); padding:22px 16px;
            border-radius:18px; font-size:1.2rem; color:black; margin:37px auto 0 auto; max-width:660px;
            font-weight:600; font-style: italic; text-align:center;}
        .new-journey-btn {display:flex; align-items:center; justify-content:center; margin:38px auto 36px auto;}
        .new-journey-btn button {background: linear-gradient(90deg, #9249d7 0%, #ff6530 100%); font-size:1.15rem;
            font-weight:700; color:#fff; border-radius:25px; padding:17px 44px; border:none; box-shadow:0 2px 12px #d1e8e255;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='journey-title'>✨ Journey Complete, {st.session_state.name} ✨</div>", unsafe_allow_html=True)
    st.markdown("<div class='journey-sub'>You have successfully completed your mental detox journey</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='summary-cards'>
        <div class='summary-card'>
            <div class='card-icon'>❤️</div>
            <div class='card-label'>Mood Addressed</div>
            <div class='card-value-orange'>{st.session_state.issue or '—'}</div>
        </div>
        <div class='summary-card'>
            <div class='card-icon'>🧠</div>
            <div class='card-label'>Steps Completed</div>
            <div class='card-value-green'>6/6</div>
            <div style='font-size:.97rem; color:#8f92ab;'>Full journey</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='journey-section'>
        <h2>Your Transformation Message</h2>
        <div style='font-size:1.18rem; color:#566c8b; margin-top:18px; font-weight:500;'>
        You've learned to breathe through anxiety and find your center. You are more resilient than you know.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='journey-list'><h2>Your Journey Today</h2>
    <div class='journey-list-item'><span class='check'>✅</span>Shared your name and opened your heart</div>
    <div class='journey-list-item'><span class='check'>✅</span>Identified and honored your current emotions</div>
    <div class='journey-list-item'><span class='check'>✅</span>Explored the roots of your feelings deeply</div>
    <div class='journey-list-item'><span class='check'>✅</span>Practiced mindful meditation for inner peace</div>
    <div class='journey-list-item'><span class='check'>✅</span>Absorbed ancient wisdom and modern guidance</div>
    <div class='journey-list-item'><span class='check'>✅</span>Released negative thoughts through sacred fire</div>
    </div>
    """, unsafe_allow_html=True)

    left, mid, right = st.columns([2, 1, 2])  
    with mid:
         if st.button("🔄 Start New Journey", key="restart", type="primary"):
                    st.session_state.step = 1

    st.markdown("""
    <div class='affirmation-section'>
        "May you be happy, may you be healthy, may you be at peace, may you live with ease."<br>
        <span style="font-size:1rem;">— Buddhist Loving-Kindness Meditation</span>
    </div>
    """, unsafe_allow_html=True)



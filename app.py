import streamlit as st
from utils.gemini import test_gemini, continue_story
import json
from utils.pollinations import get_image_url
from utils.tts import generate_audio

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="StoryScape AI",
    page_icon="📖",
    layout="wide"
)

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown("""
<div class="hero">
    <h1>📖 StoryScape AI</h1>
    <p>Create immersive AI-powered adventures with dynamic stories, artwork, and narration.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------

with st.sidebar:

    st.markdown("""
    <div class="sidebar-header">
        <h2>🎮 StoryScape AI</h2>
        <p>Create your own AI-powered visual novel</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.subheader("⚙️ Story Settings")

    genre = st.selectbox(
        "📚 Genre",
        [
            "Fantasy",
            "Adventure",
            "Mystery",
            "Horror",
            "Sci-Fi"
        ]
    )

    art_style = st.selectbox(
        "🎨 Art Style",
        [
            "Anime",
            "Realistic",
            "Pixel Art",
            "Watercolor",
            "Cyberpunk"
        ]
    )

    st.markdown("---")

    if st.button("✨ Start Your Adventure", use_container_width=True):

        with st.spinner("✨ Creating your adventure..."):

            try:
                response = test_gemini(genre, art_style)
                story = json.loads(response)

                st.session_state.story_history = [story]
                st.rerun()

            except Exception as e:
                st.error(f"❌ {e}")

    if st.button("🔄 Start New Story", use_container_width=True):
        st.session_state.story_history = []
        st.rerun()

    st.markdown("---")

    st.info(
        """
**Current Selection**

📚 **Genre:** {}
        
🎨 **Style:** {}
""".format(genre, art_style)
    )

    st.markdown("---")

    st.caption("✨ Powered by Gemini + Pollinations + gTTS")

# ---------------- Session State ----------------

if "chat" not in st.session_state:
    st.session_state.chat = None

if "story_history" not in st.session_state:
    st.session_state.story_history = []

# ---------------- Landing Page ----------------

if not st.session_state.story_history:

    st.markdown("""
    <div class="landing-page">
        <h1>🧙 Begin Your Journey</h1>
        <p>
            Every choice changes your destiny.<br>
            Select a <b>Genre</b> and <b>Art Style</b> from the sidebar,
            then begin your AI-powered adventure.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class="genre-card">
                🏰<br>
                <strong>Fantasy</strong>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="genre-card">
                👻<br>
                <strong>Horror</strong>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="genre-card">
                🚀<br>
                <strong>Sci-Fi</strong>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="genre-card">
                🕵️<br>
                <strong>Mystery</strong>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✨ Start Your Adventure", use_container_width=True):

            with st.spinner("✨ Creating your adventure..."):

                try:
                    response = test_gemini(genre, art_style)

                    story = json.loads(response)

                    st.session_state.story_history = [story]

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ {e}")

# ---------------- Gemini Test ----------------

if st.session_state.story_history:

    for index, story in enumerate(st.session_state.story_history):

        left, right = st.columns([1, 1])

        with left:
            try:
                st.image(
                    get_image_url(story["image_prompt"]),
                    width=450
                )
            except:
                st.toast("🖼️ Image server is busy, skipping visual...")

        with right:

            st.markdown(f"""
            <div class="story-card">

            <h2>📖 Scene {index + 1}</h2>

            <p>{story["story_text"]}</p>

            </div>
            """, unsafe_allow_html=True)

            if index == len(st.session_state.story_history) - 1:
                if st.button("🔊 Narrate Scene", key=f"audio_{index}"):

                    audio_file = generate_audio(story["story_text"])

                    st.audio(audio_file)
        st.divider()

    latest_story = st.session_state.story_history[-1]

    # ---------------- Story End ----------------

    if latest_story.get("is_end", False):

        st.markdown("""
        <div class="ending-screen">
            <h1>🏆 The End</h1>
            <p>Your adventure has reached its conclusion.</p>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"📖 Total Scenes: {len(st.session_state.story_history)}")

        if st.button("🔄 Start a New Adventure", use_container_width=True):
            st.session_state.story_history = []
            st.rerun()

    # ---------------- Story Continues ----------------

    else:

        st.markdown("""
        <div class="choice-title">
            <h2>🎯 What happens next?</h2>
            <p>Your decision will shape the story.</p>
        </div>
        """, unsafe_allow_html=True)

        icons = ["🧙", "🌲", "⚔️"]

        for i, option in enumerate(latest_story["options"]):

            if st.button(
                f"{icons[i]}   {option}",
                key=f"choice_{i}",
                use_container_width=True,
            ):

                response = continue_story(option)

                new_scene = json.loads(response)

                st.session_state.story_history.append(new_scene)

                st.rerun()

        if st.button(
            f"{icons[i]}   {option}",
            key=f"choice_{i}",
            use_container_width=True,
        ):
            response = continue_story(option)

            new_scene = json.loads(response)

            st.session_state.story_history.append(new_scene)

            st.rerun()
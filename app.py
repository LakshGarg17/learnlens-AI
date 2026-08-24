"""
AI Study Assistant - Streamlit Application Entry Point
Day 1: UI Scaffolding & API Connection Setup
"""

import streamlit as st
from ai_client import test_connection, get_api_key

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Sidebar: API & App Information ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.caption("Day 1: Setup & Scaffolding")
    
    # API Key status indicator & connection tester
    api_key = get_api_key()
    if api_key and api_key != "your_anthropic_api_key_here":
        st.success("🔑 API Key configured in `.env`")
    else:
        st.warning("⚠️ API Key not configured in `.env`")
    
    if st.button("🧪 Test API Connection", use_container_width=True):
        with st.spinner("Connecting to Anthropic API..."):
            result = test_connection()
            if result["success"]:
                st.success(f"Connection Successful! Response: {result['message']}")
            else:
                st.error(f"Connection Failed: {result['message']}")
    
    st.divider()
    st.markdown(
        """
        **About LearnLens AI**
        - Day 1: Project setup & UI scaffold
        - Day 2+: PDF extraction, summarization, Q&A, quiz generator, flashcards
        """
    )

# --- Main App Header ---
st.title("📚 AI Study Assistant")
st.markdown("Your intelligent companion for studying documents, articles, and complex topics.")

# --- Section 1: Upload Study Material ---
st.header("📚 Upload Study Material")
st.write("Provide your study material using either a PDF document or a topic of your choice.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload lecture notes, textbooks, or research papers.",
    )
    if uploaded_file is not None:
        st.caption(f"📄 Loaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
        # TODO: Day 2 - Extract text from uploaded PDF using pypdf

with col2:
    topic_input = st.text_input(
        "Or enter a topic manually",
        placeholder="e.g. Quantum Computing, Photosynthesis, Neural Networks",
        help="Type a subject or concept you want to study.",
    )
    if topic_input:
        st.caption(f"🎯 Target Topic: **{topic_input}**")
        # TODO: Day 2 - Prepare prompt context for manually entered topic

# --- Section Divider ---
st.divider()

# --- Section 2: Action Features ---
st.header("What would you like to do?")
st.write("Choose an action below to begin studying:")

# Four action buttons in a single row
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    summarize_clicked = st.button("📝 Summarize", use_container_width=True)

with btn_col2:
    ask_clicked = st.button("❓ Ask Question", use_container_width=True)

with btn_col3:
    quiz_clicked = st.button("🧠 Generate Quiz", use_container_width=True)

with btn_col4:
    flashcards_clicked = st.button("🗂️ Flashcards", use_container_width=True)

# --- Feature Placeholders (Day 1 UI-only Scaffolding) ---
if summarize_clicked:
    # TODO: Day 2 - wire up summarization logic here
    st.info("Feature coming soon: Document & Topic Summarization")

if ask_clicked:
    # TODO: Day 2 - wire up Q&A and interactive chat logic here
    st.info("Feature coming soon: Ask Questions & Interactive Q&A")

if quiz_clicked:
    # TODO: Day 3 - wire up quiz generation and interactive quiz grading
    st.info("Feature coming soon: AI-generated Quizzes & Knowledge Checks")

if flashcards_clicked:
    # TODO: Day 3 - wire up flashcard generator and interactive card viewer
    st.info("Feature coming soon: Interactive Study Flashcards")

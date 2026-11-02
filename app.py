import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai.errors import APIError

st.set_page_config(
    page_title="AI Career Value & Learning Roadmap",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Career Value & Learning Roadmap")
st.write(
    "Upload your photo, set your career target, and let Gemini generate "
    "your market salary range alongside a personalized, step-by-step learning roadmap."
)

# Sidebar: API Key Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Get your key at https://aistudio.google.com/"
    )
    if not api_key_input:
        st.warning("Please enter your Gemini API Key or set GEMINI_API_KEY as an environment secret.")

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. Profile Input")
    uploaded_file = st.file_uploader("Upload your photo", type=["png", "jpg", "jpeg", "webp"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    target_role = st.selectbox(
        "Target Domain / Role",
        [
            "Generative AI & LLM Engineer",
            "Machine Learning Engineer",
            "Full-Stack AI Developer",
            "Data Scientist / AI Specialist",
            "AI Product Manager"
        ]
    )

    current_level = st.radio(
        "Current Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
        horizontal=True
    )

    generate_button = st.button("Generate Roadmap & Estimate Value", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Evaluation & Roadmap")

    if generate_button:
        if not api_key_input:
            st.error("Missing Gemini API Key. Please provide it in the sidebar.")
        elif not uploaded_file:
            st.warning("Please upload a photo first.")
        else:
            with st.spinner("Analyzing profile and designing roadmap with Gemini Flash..."):
                try:
                    # Initialize Google Gen AI client with provided key
                    client = genai.Client(api_key=api_key_input)

                    prompt = f"""
                    You are an expert AI Career Coach and Tech Recruiter.
                    The user has uploaded a professional photo to evaluate their presence and wants to break into / level up as a '{target_role}' starting from a '{current_level}' level.

                    Please provide a well-structured response containing:
                    
                    ### 💼 Market Value & Price Assessment
                    - **Estimated Market Compensation / Hourly Rate**: Give realistic low, median, and top-tier salary ranges or freelance hourly rates for this specific role and experience tier.
                    - **Profile Presence Review**: Quick constructive impressions based on the provided image (lighting, professionalism, framing for tech profiles like LinkedIn/GitHub).

                    ### 🗺️ Tailored AI Learning Roadmap
                    Provide a structured milestone plan:
                    - **Phase 1: Fundamentals & Tooling** (Key topics, core libraries, math/coding foundations)
                    - **Phase 2: Core AI / ML & Architecture** (Frameworks, fine-tuning, pipelines, prompt engineering)
                    - **Phase 3: Production & Portfolio Projects** (2 concrete portfolio projects that justify high market pricing)
                    - **Recommended Free & Paid Resources** (Certifications, top docs, or community benchmarks)
                    """

                    # Call Gemini 2.5 Flash with image and text
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt, image]
                    )

                    st.markdown(response.text)

                except APIError as e:
                    st.error(f"Gemini API Error: {e.message}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")

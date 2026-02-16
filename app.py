import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Free Video to Blog AI", page_icon="📝")
st.title("🎥 YouTube Video to Blog Post Generator")

api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
youtube_link = st.text_input("Paste YouTube Video Link Here:")

video_id = None
if youtube_link:
    if "v=" in youtube_link:
        video_id = youtube_link.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
    
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg")

if st.button("Generate Blog Post"):
    if not api_key:
        st.error("Please enter API Key!")
    elif not video_id:
        st.error("Invalid YouTube link!")
    else:
        try:
            with st.spinner("Processing..."):
                # સાચો ફંક્શન કોલ
                data = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([i["text"] for i in data])

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-pro")
                prompt = f"Write a viral blog post based on this transcript: {transcript_text}"
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("Done!")
        except Exception as e:
            st.error(f"Error: {e}. Try a video that has English subtitles.")

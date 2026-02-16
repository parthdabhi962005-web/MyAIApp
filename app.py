import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Video to Blog AI", page_icon="📝")
st.title("🎥 YouTube Video to Blog Post Generator")

api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
youtube_link = st.text_input("Paste YouTube Video Link Here:")

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

if youtube_link:
    video_id = get_video_id(youtube_link)
    if video_id:
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")

        if st.button("Generate Blog Post"):
            if not api_key:
                st.error("Please enter API Key!")
            else:
                try:
                    with st.spinner("Processing Transcript..."):
                        # સીધું ફંક્શન કોલ કરવાની સાચી રીત
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                        text = " ".join([i['text'] for i in transcript])

                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(f"Write a viral blog post from this transcript: {text}")
                        
                        st.markdown("### Generated Blog Post")
                        st.write(response.text)
                        st.success("Generated Successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

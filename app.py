import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Page Setup
st.set_page_config(page_title="Free Video to Blog AI", page_icon="📝")

st.title("🎥 YouTube Video to Blog Post Generator")
st.subheader("Turn any video into a viral blog post in 1 click!")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

# Input for YouTube Link
youtube_link = st.text_input("Paste YouTube Video Link Here:")

# આ કોડ જૂની Line 17-18 ની જગ્યાએ મૂકો
if youtube_link:
    if "v=" in youtube_link:
        video_id = youtube_link.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
    else:
        video_id = None
    
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Generate Blog Post"):
    if not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar!")
    else:
        try:
            with st.spinner("Listening to the video..."):
                # 1. Get Transcript
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([i["text"] for i in transcript_list])

            with st.spinner("Writing the blog..."):
                # 2. Call Gemini AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-pro")
                
                prompt = f"""
                You are an expert content writer. 
                Summarize the following YouTube video transcript into a highly engaging blog post.
                Use bullet points, a catchy title, and subheadings.
                
                Transcript: {transcript_text}
                """
                
                response = model.generate_content(prompt)
                
                # 3. Show Output
                st.markdown("## 📝 Your Blog Post:")
                st.write(response.text)
                st.success("Done! Copy your blog post above.")

        except Exception as e:
            st.error(f"Error: {e}. Make sure the video has captions/subtitles enabled.")


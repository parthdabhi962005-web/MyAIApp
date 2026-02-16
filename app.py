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
        # ઈમેજ URL સુધારી છે
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")

        if st.button("Generate Blog Post"):
            if not api_key:
                st.error("Please enter API Key!")
            else:
                try:
                    with st.spinner("Processing Transcript..."):
                        # અહીં અમે હિન્દી અને ઇંગ્લિશ બંને ભાષા ચેક કરીએ છીએ
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                        text = " ".join([i['text'] for i in transcript_list])

                    with st.spinner("AI is writing your blog..."):
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        
                        prompt = f"Write a detailed, viral, and engaging blog post based on this YouTube video transcript. Use proper headings and bullet points. Transcript: {text}"
                        response = model.generate_content(prompt)
                        
                        st.markdown("### Generated Blog Post")
                        st.write(response.text)
                        st.success("Blog Post Generated Successfully!")
                except Exception as e:
                    st.error("Error: આ વિડિયોમાં Subtitles ઉપલબ્ધ નથી. મહેરબાની કરીને એવો વિડિયો ટ્રાય કરો જેમાં 'CC' (Subtitles) ઓન હોય.")
                    st.info("ટિપ: YouTube પર વિડિયો પ્લે કરો અને ચેક કરો કે તેમાં CC બટન કામ કરે છે કે નહીં.")

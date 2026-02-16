import streamlit as st
import google.generativeai as genai
# AttributeError થી બચવા માટે આ રીતે ઈમ્પોર્ટ કરવું જરૂરી છે
import youtube_transcript_api 
from youtube_transcript_api import YouTubeTranscriptApi

# પેજ સેટઅપ
st.set_page_config(page_title="Video to Blog AI", page_icon="📝")
st.title("🎥 YouTube Video to Blog Post Generator")

# સાઈડબારમાં API Key (ક્રેડિટ કાર્ડ વગરની ફ્રી કી)
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
        # વિડિયોનું થંબનેલ બતાવવા માટે
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")

        if st.button("Generate Blog Post"):
            if not api_key:
                st.error("મહેરબાની કરીને સાઈડબારમાં Gemini API Key નાખો!")
            else:
                try:
                    with st.spinner("વિડિયોમાંથી લખાણ મેળવી રહ્યા છીએ..."):
                        # 'hi' અને 'en' બંને ભાષા સપોર્ટ કરશે
                        # AttributeError ટાળવા માટે આ રીતે કોલ કરો:
                        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                        text = " ".join([i['text'] for i in transcript_list])

                    with st.spinner("AI બ્લોગ પોસ્ટ લખી રહ્યું છે..."):
                        # Gemini AI કોન્ફિગરેશન
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-pro")
                        
                        prompt = f"Write a professional and detailed blog post based on this transcript: {text}"
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.markdown("### 📝 Your Generated Blog Post")
                        st.write(response.text)
                        st.success("બ્લોગ પોસ્ટ તૈયાર થઈ ગઈ છે!")
                        
                except Exception as e:
                    st.error(f"એક સમસ્યા આવી છે: {e}")
                    st.info("નોંધ: ખાતરી કરો કે વિડિયોમાં સબટાઈટલ (CC) ચાલુ છે.")
